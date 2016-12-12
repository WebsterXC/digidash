# DigiDash #

## A plug-and-play digital dashboard and engine monitor. ##

### About ###
DigiDash is an auxilliary dashboard made from a Raspberry Pi and 7" RGB touchscreen, compatible with 
all OBDI-II compliant vehicles. Using a standard ELM327 OBD-II Bluetooth dongle found on sites like 
Amazon.com, users can use a Raspberry Pi to quickly and easily read and record data from their vehicle. DigiDash provides an easy to use GUI that
provides as many or as few additional gauges the driver wants to look at. The unit was designed 
with user-customizability in mind - all colors, styles, fonts, and backgrounds are configurable
for the driver and nearly every object can be repositioned with the integrated touch screen.

This project started as a semester project for CSE442 at SUNY Buffalo. The project is provided as
open-source under the GNU GPL V3 license. Enjoy!

======================================================================
### Required Hardware ###
DigiDash operates and relies on specific pieces of hardware to function properly:
* Raspberry Pi 3 (Model B) and MicroUSB Power Cable
* Official Raspberry Pi 7" Touchscreen Display
* MicroSD Card (8GB or greater preferred)
* ELM327 OBD-II Bluetooth Adapter (ELM V2.1 preferred)

In addition, we found the following items helpful during development:
* iOttie Easy One Touch 2 Car Mount for Smartphones (allows DigiDash to be mounted in a vehicle)
* 3D Printer Access (3D printer files for DigiDash case are offered)

### Downloading and Installing DigiDash ###
Thanks for downloading DigiDash! We'll walk you through getting your hardware set up 
and DigiDash running on your Raspberry Pi in no time!

For more detailed instructions, please refer to Installation.md.

### Quick Setup ###
This installation assumes you've installed Raspbian on your Raspberry Pi, and the touchscreen is
powered and connected. The DigiDash quick install is completely automated, and will take care of
downloading and installing all necessary software.

Begin by clicking on the "Clone or Download" button in the top right corner of this repository.
Navigiate to the downloaded .zip file and extract it to any directory of your choosing.

Open the folder with the extracted DigiDash files. Double-click on the file:

		install_digidash.sh

Which may prompt to to either execute the script, or execute in terminal. The first-time
installation process can easily take over 20 minutes to complete, so we reccommend
selecting "Execute In Terminal" to view the progress and ensure your RPi hasn't locked
up halfway through.

During the install process, the script will update your system, and may prompt you to download
archives. Type "Y" to continue.

		Need to get 8,689 kB of archives.
		After this operation, 9,630 kB of additional disk space will be used.
		Do you want to continue? [Y/n] Y

Similarly, it may prompt you to remove old archives. This is normal, again type "Y" to continue.

		After this operation, 887 MB disk space will be freed.
		Do you want to continue? [Y/n] Y

Wait for the script to finish running completely. Once it finishes, you can now open up a terminal and
type:

		digidash

which will start the DigiDash program. Happy driving!

=====================================================
### Group Members ###
* Will Burgin
* David Evans
* Ed Garwol
* Mark Grassi
* Joe Hanson
* Mohd Khan

### Contributing ###
Dev team communication is done through a private Slack channel. We welcome contributors, but 
currently don't have a mailing list or team contact info. To contribute to the DigiDash project,
please create an issue for your code and submit a pull request when finished. The README files
in /src and /src/can contain more technical documentation for code development.
