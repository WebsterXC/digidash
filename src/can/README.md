# CAN Communication #
---------------------
Hardware:
* ELM327 Bluetooth Receiver
* Raspberry Pi 3 - Onboard bluetooth module


### Bluetooth ###
-----------------
The Raspberry Pi 3's onboard bluetooth module was perfect wireless solution to connect to our vehicle. Traditional OBDII cables are large
and often get in the way of a driver trying to shift or brake. A generic, ELM327 OBDII unit from Amazon.com with built in bluetooth 
manages the messaging on the vehicle-side.

We had a lot of problems trying to get the ELM327 units and Raspberry Pi 3 to stay connected and communicate. After trying nearly every
combination of possible solutions, we finally settled on socket programming to be the best and most reliable way to communicate.


### CAN Data ###
----------------
Once the DigiDash unit boots it's GUI, the code checks for a valid bluetooth connection. If it finds one, it begins a background daemon that
automatically gathers vehicle data parameters (based on a preset list of common PID codes). Parameter data is stored in a global dictionary
that other files access my importing the canbus module and reading from the global dictionary. CAN data can also be gathered manually, and
the background daemon is guaranteed to yield to an explicit parameter request.

Other daemons may be started, depending on user configurations and current operating modes. These daemons utilize the Raspberry Pi's support
of multithreaded programming and process data in the background. 


### DTC Codes ###
-----------------
DigiDash not only supports the gathering and translation of Diagnostic Trouble Codes (DTC), it also offers background monitoring to alert
of possible problems as soon as they're stored in the ECU.
