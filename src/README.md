# DigiDash for Developers #
---------------------------
It seems you've dug further than the top level directory. We like your style!
The /src directory and it's subdirectories contain technical README documentation that will get
you contributing to the DigiDash project in no time!

### File Map ###
* AddGauge.py:
* DigiDash.py:
* Footer.py:
* GaugeClass.py:
* GaugeClassDigital.py:
* Header.py:
* readIn.py:
* Settings.py:
* Settings.ini:

### GUI ###
Most of the GUI files reside in this directory. DigiDash is built using sets of widgets that operate independely
of each other, allowing for the ability to create custom gauges based on input range, background styles, or even
rotation style.

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

#### Creating Custom Gauges ####

#### Changing Analog Gauge Increments ####

#### Adding Dropdown Menu Buttons ####


### DigiDash 3D Printed Case ###
