#!/usr/bin/bash
#If bluetooth module randomly locks up (usually when force closing, seems to be mostly fixed now though) run this to fix it
hciconfig hci0 down
rmmod btusb
modprobe btusb
hciconfig hci0 up
