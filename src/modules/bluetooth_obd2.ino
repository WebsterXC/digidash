#include <Timer.h>
#include <SoftwareSerial.h>

#define RxD 7                //Arduino pin connected to Tx of HC-05
#define TxD 8                //Arduino pin connected to Rx of HC-05
#define Reset 9              //Arduino pin connected to Reset of HC-05 (reset with LOW)
#define PIO11 A2             //Arduino pin connected to PI011 of HC-05 (enter AT Mode with HIGH)
#define ledpin_green A0      //Arduino output pin for Shift Light Green led 
#define ledpin_yellow A1     //Arduino output pin for Shift Light Yellow led 
#define ledpin_red 13        //Arduino output pin for Shift Light Red led 
#define sel_sw 12            //Arduino input for storing curent Shift Light RPM
#define BT_CMD_RETRIES 5     //Number of retries for each Bluetooth AT command in case of not responde with OK
#define OBD_CMD_RETRIES 3    //Number of retries for each OBD command in case of not receive prompt '>' char
#define RPM_CMD_RETRIES 5    //Number of retries for RPM command
int BinaryPins[] = {3,4,5,6};//Arduino Pins connected to 74LS47 BCD-to-7-Segment
                  //A,B,C,D//  A is LSB


unsigned int rpm,rpm_to_disp;//Variables for RPM
int shift_light_rpm;         //Variable for Shift Light RPM
boolean bt_error_flag;       //Variable for bluetooth connection error
boolean obd_error_flag;      //Variable for OBD connection error
boolean rpm_error_flag;      //Variable for RPM error
boolean rpm_retries;         //Variable for RPM cmd retries
int rpm_read = 0;
                 
SoftwareSerial blueToothSerial(RxD,TxD);
Timer t;
                  
//pin initialization
void setup()
{
   
   pinMode(RxD, INPUT);
   pinMode(TxD, OUTPUT);
   pinMode(PIO11, OUTPUT);
   pinMode(Reset, OUTPUT);
   
   digitalWrite(PIO11, LOW);
   digitalWrite(Reset, HIGH);   
   
   pinMode(3, OUTPUT);   
   pinMode(4, OUTPUT);
   pinMode(5, OUTPUT);
   pinMode(6, OUTPUT);
 
   //pinMode(ledpin_green, OUTPUT);
   //pinMode(ledpin_yellow, OUTPUT);
   //pinMode(ledpin_red, OUTPUT);
     
   pinMode(sel_sw,INPUT);
   
   rpm_retries=0;
 
   t.every(250,rpm_calc);//reads RPM value every 250ms
   
   setupBlueToothConnection();
 
   if (bt_error_flag){
     bt_err_flash();
   } 
 
   obd_init(); //initialize obd port
    
   if (obd_error_flag){
     obd_err_flash();
   }  
}


void bt_err_flash(){ //bluetooth error
   
  while(1){
    digitalWrite(ledpin_red,HIGH);
    delay(100);
    digitalWrite(ledpin_red,LOW);
    delay(100);
  }
}

void obd_err_flash(){ //obd 2 connection error
   
  while(1){
    digitalWrite(ledpin_red,HIGH);
    delay(1000);
    digitalWrite(ledpin_red,LOW);
    delay(1000);
  }
}

void rpm_calc(){ //receives raw rpm data from obd 2 and diplays it into a readable value
   boolean prompt,valid;  
   char recvChar;
   char bufin[15];
   int i;

  if (!(obd_error_flag)){                                   //if no OBD connection error

     valid=false;
     prompt=false;
     blueToothSerial.print("010C1");                        //send to OBD PID command 010C is for RPM, the last 1 is for ELM to wait just for 1 respond (see ELM datasheet)
     blueToothSerial.print("\r");                           //send to OBD cariage return char
     while (blueToothSerial.available() <= 0);              //wait while no data from ELM
     i=0;
     while ((blueToothSerial.available()>0) && (!prompt)){  //if there is data from ELM and prompt is false
       recvChar = blueToothSerial.read();                   //read from ELM
       if ((i<15)&&(!(recvChar==32))) {                     //the normal respond to previus command is 010C1/r41 0C ?? ??>, so count 15 chars and ignore char 32 which is space
         bufin[i]=recvChar;                                 //put received char in bufin array
         i=i+1;                                             //increase i
       }  
       if (recvChar==62) prompt=true;                       //if received char is 62 which is '>' then prompt is true, which means that ELM response is finished 
     }

    if ((bufin[6]=='4') && (bufin[7]=='1') && (bufin[8]=='0') && (bufin[9]=='C')){ //if first four chars after our command is 410C
      valid=true;                                                                  //then we have a correct RPM response
    } else {
      valid=false;                                                                 //else we dont
    }
    if (valid){                                                                    //in case of correct RPM response
      rpm_retries=0;                                                               //reset to 0 retries
      rpm_error_flag=false;                                                        //set rpm error flag to false
      
     //start calculation of real RPM value
     //RPM is coming from OBD in two 8bit(bytes) hex numbers for example A=0B and B=6C
     //the equation is ((A * 256) + B) / 4, so 0B=11 and 6C=108
     //so rpm=((11 * 256) + 108) / 4 = 731 a normal idle car engine rpm
      rpm=0;                                                                                            
      for (i=10;i<14;i++){                              //in that 4 chars of bufin array which is the RPM value
        if ((bufin[i]>='A') && (bufin[i]<='F')){        //if char is between 'A' and 'F'
          bufin[i]-=55;                                 //'A' is int 65 minus 55 gives 10 which is int value for hex A
        } 
         
        if ((bufin[i]>='0') && (bufin[i]<='9')){        //if char is between '0' and '9'
          bufin[i]-=48;                                 //'0' is int 48 minus 48 gives 0 same as hex
        }
        
        rpm=(rpm << 4) | (bufin[i] & 0xf);              //shift left rpm 4 bits and add the 4 bits of new char
       
      }
      rpm=rpm >> 2;                                     //finaly shift right rpm 2 bits, rpm=rpm/4
    }
      
    }
    if (!valid){                                              //in case of incorrect RPM response
      rpm_error_flag=true;                                    //set rpm error flag to true
      rpm_retries+=1;                                         //add 1 retry
      rpm=0;                                                  //set rpm to 0
      //Serial.println("RPM_ERROR");
      if (rpm_retries>=RPM_CMD_RETRIES) obd_error_flag=true;  //if retries reached RPM_CMD_RETRIES limit then set obd error flag to true
    }
}

void send_OBD_cmd(char *obd_cmd){
  char recvChar;
  boolean prompt;
  int retries;
 
   if (!(obd_error_flag)){                                        //if no OBD connection error
    
    prompt=false;
    retries=0;
    while((!prompt) && (retries<OBD_CMD_RETRIES)){                //while no prompt and not reached OBD cmd retries
      blueToothSerial.print(obd_cmd);                             //send OBD cmd
      blueToothSerial.print("\r");                                //send cariage return

      while (blueToothSerial.available() <= 0);                   //wait while no data from ELM
      
      while ((blueToothSerial.available()>0) && (!prompt)){       //while there is data and not prompt
        recvChar = blueToothSerial.read();                        //read from elm
        if (recvChar==62) prompt=true;                            //if received char is '>' then prompt is true
      }
      retries=retries+1;                                          //increase retries
      delay(2000);
    }
    if (retries>=OBD_CMD_RETRIES) {                               // if OBD cmd retries reached
      obd_error_flag=true;                                        // obd error flag is true
    }
  }
}
 
void obd_init(){
  
  obd_error_flag=false;     // obd error flag is false
  
  send_OBD_cmd("ATZ");      //send to OBD ATZ, reset
  delay(1000);
  send_OBD_cmd("ATSP0");    //send ATSP0, protocol auto

  send_OBD_cmd("0100");     //send 0100, retrieve available pid's 00-19
  delay(1000);
  send_OBD_cmd("0120");     //send 0120, retrieve available pid's 20-39
  delay(1000);
  send_OBD_cmd("0140");     //send 0140, retrieve available pid's 40-??
  delay(1000);
  send_OBD_cmd("010C1");    //send 010C1, RPM cmd
  delay(1000);
}

void setupBlueToothConnection()
{
  
  bt_error_flag=false;                   
  
  enterATMode();                          
  delay(500);

  sendATCommand("RESET");                 
  delay(1000);
  sendATCommand("ORGL");                   
  sendATCommand("ROLE=1");                 
  sendATCommand("CMODE=0");                
  sendATCommand("BIND=1122,33,DDEEFF");    
  sendATCommand("INIT");                   
  delay(1000); 
  sendATCommand("PAIR=1122,33,DDEEFF,20"); 
  delay(1000);  
  sendATCommand("LINK=1122,33,DDEEFF");    
  delay(1000); 
  enterComMode();                          
  delay(500);
}

void resetBT()
{
 digitalWrite(Reset, LOW);
 delay(2000);
 digitalWrite(Reset, HIGH);
}

void enterComMode()
{
 blueToothSerial.flush();
 delay(500);
 digitalWrite(PIO11, LOW);
 //resetBT();
 delay(500);
 blueToothSerial.begin(38400); 
}

void enterATMode()
{
 blueToothSerial.flush();
 delay(500);
 digitalWrite(PIO11, HIGH);
 //resetBT();
 delay(500);
 blueToothSerial.begin(38400);

}

void sendATCommand(char *command)
{
  char recvChar;
  char str[2];
  int i,retries;
  boolean OK_flag;
  
  if (!(bt_error_flag)){                                  
    retries=0;
    OK_flag=false;
    
    while ((retries<BT_CMD_RETRIES) && (!(OK_flag))){     
       blueToothSerial.print("AT");                       
       if(strlen(command) > 1){
         blueToothSerial.print("+");
         blueToothSerial.print(command);
       }
       blueToothSerial.print("\r\n");
      
      while (blueToothSerial.available()<=0);              
      
      i=0;
      while (blueToothSerial.available()>0){               
        recvChar = blueToothSerial.read();                 
          if (i<2){
            str[i]=recvChar;                              
            i=i+1;
          }
      }
      retries=retries+1;                                  
      if ((str[0]=='O') && (str[1]=='K')) OK_flag=true;   
      delay(1000);
    }
  
    if (retries>=BT_CMD_RETRIES) {                       
      bt_error_flag=true;                                 
    }
  }
  
}

void loop(){
  while (!(obd_error_flag)){            //while no OBD comunication error  
    if ((rpm>=0) && (rpm<10000)){       //if rpm value is between 0 and 10000 
      rpm_read = rpm; 
      
    t.update();  //update of timer for calling rpm_calc
  }
  if (obd_error_flag) obd_err_flash();
}
}
