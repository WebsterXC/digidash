# CAN Communication and Data Storage #
--------------------------------------
This directory handles all communication with the ELM327 Blueooth dongle. It provides a simple
abstraction to quickly and easily connect and read data from a vehicle's CAN bus. The /can
directory also includes files to convert and store engine parameters read from the vehicle.

### Connecting via Bluetooth ###
Connecting to the vehicle is done automatically by the canbus class on startup. DigiDash creates
a socket with the ELM327 dongle and repeatedly tries to establish a connection. While socket
programming offers a reliable connection one established, it's not uncommon for the Bluetooth
driver to require a couple of tries to open the socket.

### Interfacing with the ELM327 Dongle ###

### Sending / Receiving PIDS ###

### Converting Raw Data ###

