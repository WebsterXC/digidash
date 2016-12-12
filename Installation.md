# Installation Instructions #

This file steps you through how to setup a Raspberry Pi 3 running Raspbian Jessie to use DigiDash.
--------------------------------------------------------------------------------------------------

### Required Hardware ###
* Raspberry Pi 3 Model B
* Official Raspberry Pi 7" Touchscreen Display
* MicroSD card (Preferably at least 8GB)
* ELM327 OBDII Bluetooth Adapter (Preferably running the ELM327 v2.1 protocol)
* Micro USB cable (for powering the Pi)
* USB Keyboard (for setup only)

During development, we've also found some additional hardware helpful:
* 12V to USB Car Adapter (required if your car does not already have a USB port. Preferably at least 2 Amps.)
* iOttie Easy One Touch 2 Car Mount for iPhone & Smartphones
* Case for Raspberry Pi Official 7" Touchscreen Display (3D printer files included in DigiDash repository)
* 8 M3x6 screws

### Software Installation ###
DigiDash relies on the Raspbian Jessie operating system to run properly. For optimal boot time, we recommend
using NOOBS to handle the installation of the Raspbian OS on an SD card. Operating System installation
instructions can be found at:

	https://www.raspberrypi.org/help/noobs-setup/2/

#### Operating System Setup ####
Once Raspbian is installed, it should boot into its desktop GUI. If it does not, simply enter the following 
line into the command line interface to boot the GUI:
    
	startx

If your screen is upside-down, edit the file /boot/config.txt and add this line:
    
	lcd_rotate=2

Occasionally a small lightning bolt will appear in the top right corner of the screen. This is an undervoltage 
warning and to make it disappear, you may also add this line to the same file:
    
	avoid_warnings=1

For these changes take effect, you must reboot your system by entering the following command:
    
	sudo reboot

#### Installing Dependencies ####
Next, you must install the packages that DigiDash requires to run. Make sure that your Pi is connected to the internet. 
Then, open the terminal and enter the following lines:
    
	sudo apt-get install git python-bluez

To install Kivy:
    
	sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev pkg-config \
	libgl1-mesa-dev libgles2-mesa-dev python-setuptools libgstreamer1.0-dev git-core \
	gstreamer1.0-plugins-{bad,base,good,ugly} gstreamer1.0-{omx,alsa} python-dev cython

Then enter:

    	sudo pip install --upgrade cython
    	sudo pip install git+https://github.com/kivy/kivy.git@master

To configure Kivy to use the touchscreen as an input source, edit the file ~/.kivy/config.ini and go to the [input] section.
Add the following lines:

    	mouse = mouse
    	mtdev_%(name)s = probesysfs,provider=mtdev
    	hid_%(name)s = probesysfs,provider=hidinput

If this file doesn't exist, then save this step for later. After running DigiDash the file will be created.

All required packages have now been installed! To ensure that everything on your Pi is up-to-date, enter the following commands in your terminal:
    
	sudo apt-get update
    	sudo apt-get upgrade
    	sudo apt-get dist-upgrade
    	sudo apt-get autoremove
    	sudo rpi-update

Then reboot:
    
	sudo reboot

#### Installing DigiDash ####
To download DigiDash, open the terminal and enter the following commands:
    
	cd
    	mkdir repositories
    	cd repositories
    	git clone https://github.com/WebsterXC/digidash.git

#### Pairing your OBD-II Bluetooth Dongle ####
(This step requires you to be in or near a vehicle).
DigiDash communicates with a vehicle using an ELM327 Bluetooth dongle. To connect with the Bluetooth device, DigiDash needs
to know the device's MAC address. To add your MAC address to DigiDash:

* Plug your dongle into your car's OBDII port. 
* If no LEDs on your dongle light up, it's possible your dongle is broken or the vehicle's battery is dead. 
* On the Raspberry Pi, click on the bluetooth icon in the taskbar, then select "Add Device..." Your dongle should pop up 
in the list of devices, most likely named "OBDII".
* Select the dongle and hit "Pair." Most OBD-II dongles will prompt you for a pairing code. You should refer to your dongle's
documentation for the pairing code, but nearly nevery dongle we've tried will work with either "1234" or "0000". 
* If you now get a message saying that your dongle is paired but unusable, just ignore it.

Now, keep this terminal open and open another terminal window. In the first terminal, enter:
    
	bluetoothctl

This lists the bluetooth devices saved on your Pi. Look for your dongle in this list and note 
its MAC address. Now in the second terminal, enter the following:
    
	nano ~/repositories/digidash/src/can/blue.py

In line 26, you should see something similar to 'myMAC = "XX:XX:XX:XX:XX:XX"' where these X's are some alphanumeric characters. 
This is where the user can enter their device MAC address. Alter this line to include your own dongle's MAC address. Save your 
changes and exit this terminal with the following command:
    
	exit

You should now be back in your first terminal. Enter the following command to exit bluetoothctl:
    
	quit

#### Running DigiDash ####
It's now time to add a custom shell command to run DigiDash:
    
	cd /usr/local/bin
    	sudo nano digidash

In this new file, add the following two lines and then save:
    
	#!/bin/bash
	sh -c 'cd ~/repositories/digidash/src/ && exec python main.py'

Now, make this file executable:
    
	sudo chmod +x digidash

#### Autorun on Startup ####
If you're using your Pi exclusively for DigiDash, and would like it to start DigiDash immidiately on system startup, perform
the following commands to include DigiDash in Raspbian's startup routine:

To set DigiDash to auto-run on startup:

    	sudo nano /etc/profile

Scroll to the bottom and add the following line:
    
	digidash

Lastly, you must set your Pi to boot to the command line. Not only does this speed up boot time, we highly recommend using DigiDash
as the master GUI frame to avoid conflictions with the underlying desktop. Open the Pi's home drop-down menu, then choose 
"Preferences"->"Raspberry Pi Configuration". Select "Boot: TO CLI" and then hit OK.

Should you want to run DigiDash manually from it's entry point, navigate to the /src directory and type:

		sudo python main.py

Which will invoke DigiDash manually. Note that DigiDash can be run without superuser priveledge, however it will annoyingly ask
you if you'd like to remove the previous .log file (of course you do!).

### You're now good to go! Reboot you Pi and experience some good ol' DigiDash fun! ###
