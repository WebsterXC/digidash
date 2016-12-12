#These should add those two line to the beginning of config.txt file
sed -i '1 a lcd_rotate=2' /boot/config.txt
sed -i '1 a avoid_warnings=1' /boot/config.txt

#sed -i '1 a lcd_rotate=2' ~/config.txt
#sed -i '1 a avoid_warnings=1' ~/config.txt

#Install git and bluez
sudo apt-get install git
sudo apt-get install python-bluez

#Install dependencies for Kivy
#If they are already installed, it should skip over them or update if old version installed
sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev pkg-config libgl1-mesa-dev libgles2-mesa-dev python-setuptools libgstreamer1.0-dev git-core gstreamer1.0-plugins-{bad,base,good,ugly} gstreamer1.0-{omx,alsa} python-dev cython
sudo pip install --upgrade cython
sudo pip install git+https://github.com/kivy/kivy.git@master

#Insert call to python script to change kivy ini file
#HERE

#Update System
sudo apt-get update
sudo apt-get upgrade
sudo apt-get dist-upgrade
sudo apt-get autoremove
sudo rpi-update

#Clone DigiDash
cd
mkdir repositories
cd repositories
git clone https://github.com/WebsterXC/digidash.git


#We should really do a reboot now but then we cant run digidash automatically
#Maybe before reboot setup the auto start stuff
#sudo reboot




