# DigiDash for Developers #
---------------------------
It seems you've dug further than the top level directory. We like your style!
The /src directory and it's subdirectories contain technical README documentation that will get
you contributing to the DigiDash project in no time!

### File Map ###
* AddGauge.py: Provides utilities to build individual gauge objects for each PID. 
* AddGauge.csv: Defines all the possible gauges that DigiDash supports (for menu integration).
* DigiDash.py: GUI boot point. File takes all built objects and places them on the screen.
* Footer.py: File defines the time/date footer that's on DigiDash's home screen.
* GaugeClass.py: File defines the analog gauge class, gauge appearences, and functions to interact with it.
* GaugeClassDigital.py:	File defines the digital gauge class, gauge appearences, and functions to interact with it.
* Header.py: File is used to create an optional header for the DigiDash home screen. It is currently disabled.
* readIn.py: Contains a utility to read in data to DigiDash from various CSV files.
* Settings.py: All the methods bound to the buttons in the Settings dropdown menu. 
* Settings.ini: File that defines the state of gauges on the home screen at boot time.

### GUI ###
Most of the GUI files reside in this directory. DigiDash is built using sets of widgets that operate independely
of each other, allowing for the ability to create custom gauges based on input range, background styles, or even
rotation style. DigiDash uses Kivy, an open-source Python GUI library to handle all touch and display events.

#### Settings Initialization File ####
The Settings.ini file is used to populate the GUI on every boot. The file defines each gauge that should be placed
on the home screen at startup, and correspondingly adds those gauges to the automatically updated PID list. The
Settings file also defines the positions of each gauge, their type and style, as well as the minimum and maximum
values possible for each parameter.

#### Changing Brightness ####
DigiDash's touchscreen brightness can by changed at runtime, using a short Bash script that writes a brightness value
to a system file in the operating system. If the user is running the intended Raspbian OS, the brightness changing
feature should work as intended, but due to different brightness values on different operating systems, any other
Linux distribution may not change the brightness as intended.

The brightness changing feature can be access via a dropdown menu on the home screen. Since the Raspberry Pi requires
an internet connection to update it's system clock, and a DigiDash unit would rarely have a WiFi connection while
driving, the unit does not automatically change the brightness based on time of day.

### Home Screen ###
The DigiDash home screen is completely user configurable. Using a touchscreen, all gauges can be picked up and
placed anywhere on the screen. They can be resized, recolored, restyled, and deleted all with no more than two
screen touches. In addition, the home screen background can be changed to any image the user desires.

The DigiDash home screen is invoked through DigiDash.py. Reading from the Settings.ini file, it creates Gauge widgets
for each gauge required by the user at startup. After defining a background, it loads all dropdown menus and places the
gauges on the screen. Gauges are automatically updated by reading from the global canbus.CANdata dictionary. Gauges
should *never* request data from the CAN bus explicitly.

#### Adding Custom Backgrounds ####
Any .jpg or .png image can be used as a home screen background for DigiDash. The software will automatically scale the
image to the appropriate physical size if it's not exactly 800x480, however the aspect ratio is not maintained. For
optimal results, use an exact-fit image for the home screen.

To add a background, place the image in:
		/src/Images

Create Gauge background button/dropdown in Settings.py
Add an instance of the BG afterwards

#### Adding New Gauges ####
DigiDash offers two classes of gauges, analog and digital, which can be modified by the developer. Each gauge is built
and placed from the same code, so once the gauge functionality is programmed by the developer the gauge will
be available in both analog and digital format. Values for the gauges, including PID, minimum value, maximum value,
and even color are all imported from the Settings.ini file at startup. 

#### Changing Analog Gauge Increments ####
For analog gauges (GaugeClass.py), it's common to need change the interval on the gauge markings. To do so, navigate
to lines 409-414 in GaugeClass.py. To define a new range of values:

		val_range = self.MaxValue-self.MinValue

Where val_range is an integer representing the number of discrete increments. To change the angle of rotation for the
analog gauges:

		angle = 360 - (scale*val)

Where val represents the current parameter value passed to the setVALUE(...) function. Based on the scale that
was generated earlier from the value range, DigiDash calculates the angle required of the needle of the analog
gauge on the screen that properly represents the value of the actual parameter in the backend. For most
applications, the default angle calculation and gauge scaling works great.

Note the line that updates the value of the gauge:

		val = canbus.CANdata[self.PID]

Gauges are aware of the PID they represent to index the global CAN dictionary that holds the most recent value
of the engine paramter. *Under no circumstances* should a gauge communicate with the CAN bus directly - instead
it should be updated through the CAN dictionary. Of course, gauges should never write to this data structure.
Recall that gauges automatically begin updating their internal value as soon as it's added to the home screen, either
during startup or manually via the dropdown menu (see the README.md file in the /can directory for more detail).

#### Modifying Digital Gauges ####
For digital gauges, you should refer to the GaugeClassDigital.py file. Although digital gauges aren't very
configurable beyond color and style, it's possible to physically reshape the gauge with a custom image. DigiDash
digital gauges (and some analog gauges) are a background gauge image set behind updating text; to change the
digital gauge shape is as simple as changing the image file that Kivy uses to create a Gauge object. In
GaugeClassDigital.py, navigate to line 48:

		self.gauge = Image(source='Images/Gauges/GaugeSquare1.png', size(400,400))

Where the source file is the background image to build a digital gauge from. Since gauges are naturally resizable,
the size argument should be left as-is to ensure reverse compatibility. All images should be kept in the /Images
directory.

#### Adding Dropdown Menu Buttons ####
In many cases, the gauges need to be added to the screen during runtime, and to be able to add this functionality
to your custom gauge, a button needs to be added to the home screen dropdown menu. However, this process has 
been automated by editing a simple text file. The entries take the format:

		<Name>,<Min>,<Max>,<Units>,0x<PID>

To add a new gauge entry, navigate to the /src directory and run the command:

		cat '<Name>,<Min>,<Max>,<Units>,0x<PID>' >> AddGauge.csv

Where Name represents the title to display on the gauge, Min is the minimum value possible for this parameter,
and Max is the maximum value. Units represents the units that the parameter is measured in however since all
DigiDash math accounts for unit conversions, the Units variable is read in as a literal string and displayed 
directly to the gauge, similar to Name.

### 3D Printed Case ###
In addition to the software, we designed and printed our own case for the DigiDash unit. It provides a relatively
inexpensive case solution for the fragile Pi and touchscreen, and is even designed to fit and mount into standard
GPS/phone mounts found on Amazon.com. The case considers the positioning of Ethernet, USB, and provides proper
ventilation under high load.

The case is easy to use, as it only requires 3 separate pieces and 8 screws. It's even sturdy enough to withstand
a significant impact from ceiling height (just trust us on this here, don't try this at home)! The model files can
be found in the /3dprinting directory and can be uploaded to nearly every 3D printer on the market.
