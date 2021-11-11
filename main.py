#!/usr/bin/python3

#Starts things up and runs the threads

import time
import logging
from config import DEBUG_LEVEL

##LOGGING STUFF TO RUN STRAIGHT UP##
logging.basicConfig(format='%(asctime)s - %(levelname)8s - %(filename)13s - %(threadName)10s: %(message)s', level=DEBUG_LEVEL)

logger = logging.getLogger('main')
logger.info('Logging started')

#set level for pygatt and webserve (want to separate webserve)
logging.getLogger('pygatt').setLevel(logging.WARNING)
logging.getLogger('flask').setLevel(logging.WARNING)

import mqtt
import bleserve
import webserve
import threading
from config import *

if __name__ == '__main__':
    try:
        pill2kill = threading.Event()
        command_added = threading.Event()
        status_changed = threading.Event()
        if WEB_ON:
            logger.info('Web thread starting')
            threadweb = threading.Thread(name='Web Server', target=webserve.start_server, args=(pill2kill, command_added))
            threadweb.setDaemon(True)
            threadweb.start()
        logger.info('Bluetooth thread starting')
        threadble = threading.Thread(name='BLE Server', target=bleserve.start_bleak, args=(pill2kill, command_added, status_changed, ))
        threadble.start()
        if MQTT_ON:
            logger.info('MQTT thread starting')
            threadmqtt = threading.Thread(name='MQTT', target=mqtt.main_mqtt, args=(pill2kill, command_added, status_changed, ))
            threadmqtt.start()
        while True: 
            time.sleep(5) #needed to keep exception catching alive
    except KeyboardInterrupt:
        logger.error("Ctrl-C Caught Shutting Down")
        pill2kill.set()
        threadble.join()
        if MQTT_ON:
            threadmqtt.join()
    finally:
        logger.warning("Shutdown Complete")


