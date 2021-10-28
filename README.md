# Yamaha SR-C20A

This is a python script to interact with the Yamaha SR-C20A soundbar via BLE. It uses pygatt to connect and maintain a BLE connection to the soundbar imitating the "Sound Bar Remote" app from yamaha.

It creates both a web and mqtt interface for interacting with the soundbar and obtaining its status. The MQTT interface is useful for interacting with the soundbar in Home Assistant which was the original reason I put this together.

All thanks to the excellent work by Michal Jirku who posted an excellect [blog post series](https://wejn.org/2021/04/multi-weekend-project-reversing-yamaha-yas-207-remote-control/) on reverse engineering the YAS-207 soundbar. That one uses bluetooth and a different yamaha app, the underlying protocol turned out to be very similar, see here for his [project repo](https://github.com/wejn/yamaha-yas-207).
## Use

Download and extract the code. Copy config.py.example to config.py and edit the contents. You will need to pip3 install pygatt paho-mqtt flask. Then run main.py.

I developed and tested this on ubuntu linux 21.04 using the builtin bluetooth module of an ASUS PN-50.

I only have one soundbar to test on so I'm not sure what specifics might need to change for each soundbar.

I suspect these scripts could be adapted to work with other Yamaha soundbars using the same app but each soundbar will have additional or lesser functionality.

### Web Interface

You can access soundbar status through http://[ip]:[port]/status where ip and port are set in config.py you can issue commands to http://[ip]:[port]/do/[command] where command is the command you would like to send to the soundbar, these are all found in function.py. You can also set the volume to a specific level with http://[ip]:[port]/do/volumeSet?vol=[volume] where volume is a number 0-100.

### MQTT Interface

Read the mqtt.py file for details of the topics that are published and subscribed to and relevant values.

## Credits

* Author: Michael Obst
* Inspiration and protocol reverse engineering: Michal Jirku (wejn.org)

## Licence

GNU Affero General Public License v3.0
