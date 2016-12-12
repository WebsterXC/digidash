# CAN Communication and Data Storage #
--------------------------------------
This directory handles all communication with the ELM327 Blueooth dongle. It provides a simple
abstraction to quickly and easily connect and read data from a vehicle's CAN bus. The /can
directory also includes files to convert and store engine parameters read from the vehicle.

### File Map ###
* automath.py: Defines functions to convert from raw hexadecimal CAN data to usable decimal values.
* blue.py: Coordniates bluetooth communication by sending ASCII chars over a socket connection.
* canbus.py: Class holds all engine data and provides abstractions for the Bluetooth conenction.
* canfunctions.py: Contains functions used to simulate dynamometer/tuning results.
* daemon.py: Contains background threads that perform cyclic, I/O-bound tasks.
* dtc.py: Handles vehicle status and gathering / clearing of diagnostic trouble codes.
* pids.py: Establishes macros for common OBDII PID codes.

### Bluetooth Communication ###
DigiDash communicates with the ELM327 bluetooth dongle by socket programming. We found that this was
more reliable and easier to configure than the serial object counterpart.

#### Interfacing with the Bluetooth Dongle ####
As the file map suggests, all of the core Bluetooth code resides in blue.py. However, we've abstracted
the sending and receiving of raw characters and deferred the functionality to the canbus class in
canbus.py. Even if the canbus object has not been created, a user can still communicate with the dongle.

	canbus.send_command(mode, pid)

Where the mode represents the subsystem the command is intended for and the PID is the command to send.
* mode: These are defined in pids.py, but the only possible options are MODE_ELM(0x00) and MODE_DTC(0x03).
* pid: Is a PID to send the DTC subsystem. If MODE_ELM is used, this represents the ELM327 command.

On startup, the canbus class calls this method twice to reset the dongle (ATZ) and to turn off echoes (ATE0).
This method is thread safe, and will always return even if a background daemon is running. Since ELM
dongles vary widely, it does not filter user input and this method should be called with care.

#### Sending and Receiving OBD-II PIDs ####
DigiDash provides two different utilities to collect engine parameters from the vehicle. To manually
request an OBD-II PID, the canbus class constructs an ELM327 formatted message to request the correct
parameter from the CAN bus. After waiting for a response, the raw bytes from the CAN bus are returned
as a string.

	canbus.send_pid(pid):

Where the pid represents a standard OBD-II PID in string format, preferably from the pids.py macros.

Since raw bytes are returned, the result must be filtered into the automath.convert() function to get
a usable value. Where possible, an individual function should be used for each PID code for the fastest 
runtime.

Since this method interrupts the connection of the CANDaemon, it should not be called in a loop. If the
value of a PID is needed constantly, such as the on-screen gauges, it should be passed to the automatic
parameter background daemon:


The CANDaemon in daemon.py is started in DigiDash's main.py entry point. The CANDaemon handles the automatic
gathering of engine parameters that are needed constantly, such as on-screen gauges. Since it acts as a
background thread, it allows DigiDash to maintain a responsive GUI by reading the most recent data from
a common global data structure (Python dictionary) rather than waiting for each individual response from
the ELM327 dongle. Therefore, when gauges are added to the screen, the corresponding PID is added to the
list that the CANDaemon cyclically reads from to establish auto-update gauges.

To ready a PID for automatic updating, it needs to be added to the PIDcodes list residing in the canbus.py
file. However, *the PID should not be added manually* because the global dictionary must be informed of the
new PID by adding it's entry into the dictionary. The subscribe method is provided to coordniate this:

	canbus.subscribe(pid)

Where PID represents a standard OBD-II PID in string format, preferably from the pids.py macros. After
adding the PID, the most recent value returned from the CAN bus for that PID is automatically placed in:

	canbus.CANdata[pid]

Where pid is a standard OBD-II. It is important to use macros from pids.py to avoid dictionary KeyErrors.

### CAN Bus Abstraction ###
The canbus class is an abstraction of the code used to send characters back and forth from the ELM327 dongle.
In addition to a clean GUI, we wanted to create an easy to use "API" for future development. As a result, the
canbus class takes care

On startup, the canbus class attemps to establish a Bluetooth connection by first creating a bluetooth object,
and then calling Blue.connect().The socket programming code in blue.py will attempt to connect to the vehicle
5 times, 5 seconds apart. If all 5 tries fail, DigiDash gives up and exits (see "Troubleshooting Connections"
below).

If a vehicle is available, the canbus class first resets the ELM327 dongle with the ATZ command; this clears 
registers and resets the device's baud rate. We've found that resetting the dongle before each session provides 
a more reliable connection. The canbus class also turns off echoes; traditionally the ELM327 dongle would "confirm" 
the command you send it by first responding with the sent characters and then the response for the vehcile. Not 
only does this waste precious communication speed, it's irrelevant for our implementation, and is turned off by 
sending the ELM327 dongle the ATE0 command.

The canbus class has now started up and passes control the the CANDaemon.

#### Automatic Data Gathering ####
DigiDash offers automatic data gathering in the form of a background daemon. The CANDaemon is implemented to
constantly iterate over a list of PIDs, and for each, request it's PID from the CAN bus over the bluetooth
connection. The CANDaemon is central to DigiDash's core functionality - it enables automatic updating of
gauges and prevents unexpected connection timeouts since the port is always being used.

The downside to always using to the port is response time. As the list of automatically updated PIDs increases
(the user puts a lot of gauges on the screen, or a deveoper implements code that requires a lot if information),
the speed at which each can be updated significantly reduces. In addition to the extra bus usage, the underlying
Raspbian operating system is being relied on to schedule DigiDash's threads with enough priority to maintain a
responsive GUI, and with a large list of automatically updated PIDs this responsiveness is seriously affected.
Therefore, developers should always consider the impact that each requested PID makes on the overall system when
adding new features.

#### Converting Raw Data ####
The ELM327 dongle returns strings of hexadecimal characters representing engine parameters because that's the
way the CAN bus expresses information publicly. Unfortunately, not all PID codes can be converted to decimal
values with the same mathematical formula, and not all PIDs return the same number of bytes either. The automath.py
file contains a long list of functions to convert the individual bytes to actual usable values. Individual functions
are used for the fastest runtime possible, because many of these conversion calculations are performed by the CANDaemon
in between messages.

Using a conversion function requires the developer to know which bytes of data are relevant in the CAN bus response. A
typical transaction might look like:

		canresponse = canbus.send_pid(pids.ENG_RPM)

The canresponse variable now holds a string representing the ELM327 dongle's response. A valid response looks similar to:

		"41 0C BE 1F B8 10"

Which is a great response, because we can confirm it's correct. The first byte, 0x41, represents the mode in which the
CAN bus was pinged (41 represents Mode 01, realtime gathering mode). The second byte, 0x0C, replies the PID the response
bytes correspond to. Referring to the OBD-II specification, a request for RPM returns 4 bytes, which are the remaining
bytes in the list above. We can label these individual bytes A, B, C, and D. To convert from hexadecimal to rev/min, we
pass bytes A and B to the corresponding function in automath.py:

		automath.eng_rpm_conv(A, B)

Where A = "BE" and B = "1F" (for this example). Note that the mathematical functions to convert hex to decimal values are
defined by the OBD-II protocol specification (we didn't make them up).

The CANDaemon is one particular instance where the code knows the PID of the parameter, but has no idea which conversion
function to use. To circumvent this, a dictionary of PIDs to conversion functions is provided in the automath.py
file, and an auto-lookup function provided as automath.convert(...). In fact, this function also takes care of splitting
the reutrn string and idenfying which bytes are relevant for the PID requested. To automatically convert:

		automath.convert(pid, raw)

Where pid is the OBD-II PID and raw is the string of raw hexidecimal bytes returned by canbus.send_pid(). This function
will then split the data and determine the correct conversion function and correct bytes based on the pid argument. Note 
that this function has a much slower runtime than the individual functions, and should only be used when the code can not 
make a connection between PID and engine parameter name.

### Diagnostic Trouble Codes ###
Central to any OBD-II interfacing device is the ability to clear the pesky check engine light on the physical vehicle
dashboard.

#### Reading Codes ####
DigiDash has the ability to read DTC codes and look up an English translation for what caused
the fault. To get the currently active trouble codes:

		dtc.dtc_scan()

The method takes no arguments and returns a list of DTC codes in the standard trouble code format (one character plus a
4-digit code). 

#### Clearing Check Engine Light ####
To clear the active codes, including the check engine light, simply call:

		dtc.dtc_clear()

Again, this method takes no arguements and tells the vehicle to clear all current DTC trouble codes, and to turn off all
MILs (including the check-engine light). The method provides a 0.5 second delay to give the vehicle's CAN bus a chance to
finish clearing all codes in memory, and then returns nothing.

### Dynamometer Functions ###

#### Drivetime Logging ####
DigiDash supports drivetime logging to a text or CSV file, and references the same canbus.PIDcodes list that the CANDaemon
does. This allows users to go for a drive and have the ability to review their data when their finished using DigiDash.
The LoggerDaemon has a completely configurable sample time for various applications and a resizable RAM buffer to delay 
the length I/O transactions that writes incur. The current implementation writes a line of data to a comma-delimited (CSV) 
text file, where each line contains the data for each PID in canbus.PIDcodes.

To start the basic logging service, navigate to main.py and uncomment the two lines that start the LoggerDaemon:

		p = daemon.LoggeerDaemon()
		p.start()

However, for many applications, the file location may vary or need to be changed. Navigate to the /can directory
and open the daemon.py file. The file location is defined on line 143:

		log_data_to_file = "can/data/runtime.txt"

To change the sampling time or size of the RAM buffer, the arguments for the logging thread should be changed. In the
LoggerDaemon class, on line
		
		canlogging_process(64, 0.1)
		
The first argument (64) specifies the number of CSV lines to store in RAM before initiating a write flush for the entire
buffer. The second argument (0.1) specifies the sampling time - a line of data is recorded from canbus.CANdata every 0.1
seconds.

#### Running Tests ####
It's possible to simulate the functions of a standalone tuning dynamometer using many of the runtime tests found in canfunctions.py,
including estimated torque-to-weight ratios, optimal upshift points for each gear, and max horsepower. Runtime tests take
over the home screen with their own window, and are active during the duration of the test. In an effort to make the dyno
tests as simple as possible, many of them can be started from any engine state, and wait for specific vehicle sensor values
before continuing. Possible tests and calculations include:
<<<<<<< HEAD
=======

>>>>>>> a8280114f7641c6ee0fdd3d16bebdaa8bdec8abc
* Simulating a 4th gear dyno pull to calculate max horsepower. 
* Optimal shift points (in RPM) for each gear.
* 0-60MPH acceleration time.
* Quarter mile pull time, speed, and approximate max horsepower.
* Dynamometer correction factor (for use on a real tuning dyno).

Note that since many other forces are at play driving on the road versus a dyno, the calculations performed by canfunctions.py
should be considered estimates. A standard tuning dynamometer provides near-optimal traction and low resistance which our math
does not compensate for.

### Additional Development Utilities ###

#### Debug Logging ####
DigiDash offers debug logging for development using the logging module available in the standard Python distribution. The module
prioritizes output messages, all of which are written to /src/can/data/digilog.log. The standard DigiDash release filters all
messages that aren't errors or considered critical, but can be changed for testing and development.

Starting the logging module to log to a file happens at first boot, and the closing of the file happens when DigiDash exits. However,
if DigiDash is not closed properly or an error is not handled, the log file may not save.Therefore, an exit routine method is offered 
to group all necessary shutdown tasks in case DigiDash must close in an exception handler.

The current format of the log messages is [timestamp] | [message], but can be changed in main.py. Please use the following priority
conventions:
* log.debug (Priority 10): Reserved for writing raw data to the logging file. (Example: raw bytes from a CAN message)
* log.info (Priority 20): Generic DigiDash messages.
* log.warning (Priority 30): Messages more important than log.info, but would not cause DigiDash to exit or stop running.
* log.error (Priority 40): Messages that could possibly cause DigiDash to stop running if not handled correctly. 
* log.critical (Priority 50): Events that prevent DigiDash from continuing to run.

#### Offline Development & Vehicle Simulation ####
Most of us realized very quickly that programming inside of, or near your vehicle can be difficult or impossible, especially in
adverse weather conditions. To enable development without a vehicle, /can/data/data.txt provides a set of sample input data that 
can be fed into DigiDash's data structures to simulate a real vehicle driving.

The ParserDaemon is a background daemon offered for just this purpose. It takes the place of the CANDaemon - the parser fills the
global CANdata dictionary structure in the same way the CANDaemon does, but instead of using a Bluetooth connection to the vehicle, 
it uses values found in the CSV text file. The result is the ability to test new code intended for realtime deployment, unchanged 
on a local system. To enable offline development, a few steps are required.

First, we need to turn off Bluetooth. If you don't do this, DigiDash will exit due to a nonexistent connection. In canbus.py, lines 42
and 43 should look like:

		#BlueObject.connect()
		print("Fake Connection!")

This allows DigiDash to continue without trying to establish a bluetooth connection. The print statement is required, since it's now
the only line inside of a try-except block.

Next we need to replace the CANDaemon with the ParserDaemon, but only temporarily. In main.py, comment the two lines that start the
CANDaemon and uncomment the lines that start the ParserDaemon. It should look like:

		#d = daemon.CANDaemon()
		#d.start()
		d = daemon.ParserDaemon()
		d.dstart()

Of course, this should be changed back when deploying DigiDash to a real vehicle again.

### Troubleshooting, etc... ###

##### My Bluetooth dongle won't connect! #####
We've found that the messages returned by the Bluetooth socket module are pretty much garbage.
Similarly, the standard Amazon.com "OBD-II Bluetooth Dongle" is a generic OEM clone of the same
product, any many brand new units don't communicate correctly.

* Check to ensure the MAC address you entered for your Bluetooth dongle in blue.py is correct. If
you never performed this step, check out Installation.md in the top-level directory for detailed
instructions on how to do this.

* Try rebooting your Raspberry Pi. If DigiDash closes without running it's exit routines, occasionaly
the Bluetooth socket does not close correctly and makes reconnecting very troublesome. Sometimes
closing the terminal that DigiDash is running in (if applicable) will force the socket closed without
needed a reboot.

* Try getting closer to the vehicle. If you're like us, and developing DigiDash in the comfort of our 
homes, it's very easy to not be able to connect on the first couple of tries since you're so far away.
Distance, walls, foliage, and weather can all affect your connection to the Bluetooth dongle, all of
which would not exist inside a vehicle.
