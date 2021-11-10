#Called as a thread to run the MQTT server

from config import *
import paho.mqtt.client as mqtt
import logging

logger = logging.getLogger(__name__)

published = yam()

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        logger.info("Connected to MQTT Broker OK Returned code=" + str(rc))
    else:
        logger.warning("Bad connection Returned code= " + str(rc))

def on_message(client, userdata, message):
    logger.debug("Message received " + str(message.payload.decode("utf-8")))
    logger.debug("Message topic=" + message.topic)
    logger.debug("Message qos=" + str(message.qos))
    logger.debug("Message retain flag=" + str(message.retain))

    msgdata = str(message.payload.decode("utf-8"))
    if message.topic == 'yamaha/power/switch':
        if msgdata == 'True': command_queue.put(['powerOn'])
        elif msgdata == 'False': command_queue.put(['powerOff'])
        else: logger.warning('Bad data in mqtt topic ' + message.topic + ': ' + str(msgdata))
    elif message.topic == 'yamaha/mute/switch':
        if msgdata == 'True': command_queue.put(['muteOn'])
        elif msgdata == 'False': command_queue.put(['muteOff'])
        else: logger.warning('Bad data in mqtt topic ' + message.topic + ': ' + str(msgdata))

    elif message.topic == 'yamaha/input/switch':
        if msgdata == 'TV': command_queue.put(['inputTV'])
        elif msgdata == 'Bluetooth': command_queue.put(['inputBluetooth'])
        elif msgdata == 'Optical': command_queue.put(['inputOptical'])
        elif msgdata == 'Analog': command_queue.put(['inputAnalog'])
        else: logger.warning('Bad data in mqtt topic ' + message.topic + ': ' + str(msgdata))
    elif message.topic == 'yamaha/input/tv':
        if msgdata == 'True': command_queue.put(['inputTV'])
        elif msgdata == 'False': pass
        else: logger.warning('Bad data in mqtt topic ' + message.topic + ': ' + str(msgdata))
    elif message.topic == 'yamaha/input/bluetooth':
        if msgdata == 'True': command_queue.put(['inputBluetooth'])
        elif msgdata == 'False': pass
        else: logger.warning('Bad data in mqtt topic ' + message.topic + ': ' + str(msgdata))
    elif message.topic == 'yamaha/input/optical':
        if msgdata == 'True': command_queue.put(['inputOptical'])
        elif msgdata == 'False': pass
        else: logger.warning('Bad data in mqtt topic ' + message.topic + ': ' + str(msgdata))
    elif message.topic == 'yamaha/input/analog':
        if msgdata == 'True': command_queue.put(['inputAnalog'])
        elif msgdata == 'False': pass
        else: logger.warning('Bad data in mqtt topic ' + message.topic + ': ' + str(msgdata))

    elif message.topic == 'yamaha/sub_up/switch': 
        if msgdata == 'True': command_queue.put(['subUp'])
        else: logger.warning('Bad data in mqtt topic ' + message.topic + ': ' + str(msgdata))
    elif message.topic == 'yamaha/sub_down/switch': 
        if msgdata == 'True': command_queue.put(['subDown'])
        else: logger.warning('Bad data in mqtt topic ' + message.topic + ': ' + str(msgdata))

    elif message.topic == 'yamaha/volume/switch': 
        logger.error(['volumeSet', min(max(0, int(msgdata)), 50)])
        if int(msgdata): command_queue.put(['volumeSet', min(max(0, int(msgdata)), 50)])
        else: logger.warning('Bad data in mqtt topic ' + message.topic + ': ' + str(msgdata))
    elif message.topic == 'yamaha/vol_up/switch': 
        if msgdata == 'True': command_queue.put(['volUp'])
        else: logger.warning('Bad data in mqtt topic ' + message.topic + ': ' + str(msgdata))
    elif message.topic == 'yamaha/vol_down/switch': 
        if msgdata == 'True': command_queue.put(['volDown'])
        else: logger.warning('Bad data in mqtt topic ' + message.topic + ': ' + str(msgdata))

    elif message.topic == 'yamaha/style/switch':
        if msgdata == 'Standard': command_queue.put(['standardMode'])
        elif msgdata == 'Movie': command_queue.put(['movieMode'])
        elif msgdata == 'Game': command_queue.put(['gameMode'])
        else: logger.warning('Bad data in mqtt topic ' + message.topic + ': ' + str(msgdata))
    elif message.topic == 'yamaha/style/standard':
        if msgdata == 'True': command_queue.put(['standardMode'])
        else: logger.warning('Bad data in mqtt topic ' + message.topic + ': ' + str(msgdata))
    elif message.topic == 'yamaha/style/movie':
        if msgdata == 'True': command_queue.put(['movieMode'])
        else: logger.warning('Bad data in mqtt topic ' + message.topic + ': ' + str(msgdata))
    elif message.topic == 'yamaha/style/game':
        if msgdata == 'True': command_queue.put(['gameMode'])
        else: logger.warning('Bad data in mqtt topic ' + message.topic + ': ' + str(msgdata))
    elif message.topic == 'yamaha/surround/switch':
        if msgdata == 'True': command_queue.put(['surroundMode'])
        else: logger.warning('Bad data in mqtt topic ' + message.topic + ': ' + str(msgdata))

    elif message.topic == 'yamaha/bass/switch':
        if msgdata == 'True': command_queue.put(['bassOn'])
        elif msgdata == 'False': command_queue.put(['bassOff'])
        else: logger.warning('Bad data in mqtt topic ' + message.topic + ': ' + str(msgdata))
    elif message.topic == 'yamaha/clear_voice/switch':
        if msgdata == 'True': command_queue.put(['clearVoiceOn'])
        elif msgdata == 'False': command_queue.put(['clearVoiceOff'])
        else: logger.warning('Bad data in mqtt topic ' + message.topic + ': ' + str(msgdata))

    elif message.topic == 'yamaha/led/switch':
        if msgdata == 'Bright': command_queue.put(['ledBright'])
        elif msgdata == 'Dim': command_queue.put(['ledDim'])
        elif msgdata == 'Off': command_queue.put(['ledOff'])
        else: logger.warning('Bad data in mqtt topic ' + message.topic + ': ' + str(msgdata))
    elif message.topic == 'yamaha/led/bright':
        if msgdata == 'True': command_queue.put(['ledBright'])
        else: logger.warning('Bad data in mqtt topic ' + message.topic + ': ' + str(msgdata))
    elif message.topic == 'yamaha/led/dim':
        if msgdata == 'True': command_queue.put(['ledDim'])
        else: logger.warning('Bad data in mqtt topic ' + message.topic + ': ' + str(msgdata))
    elif message.topic == 'yamaha/led/off':
        if msgdata == 'True': command_queue.put(['ledOff'])
        else: logger.warning('Bad data in mqtt topic ' + message.topic + ': ' + str(msgdata))
    else:
        logger.warning("Unknown message topic: " + message.topic + " : with data: " + str(msgdata))

def publisher(client):
    if published.power != yam1.power: 
        client.publish("yamaha/power", yam1.power, retain=True)
        published.power = yam1.power
    if published.input_source != yam1.input_source: 
        client.publish("yamaha/input", yam1.input_source_name, retain=True)
        client.publish("yamaha/input/tv/state", str(yam1.input_source_name == "TV"), retain=True)
        client.publish("yamaha/input/bluetooth/state", str(yam1.input_source_name == "Bluetooth"), retain=True)
        client.publish("yamaha/input/optical/state", str(yam1.input_source_name == "Optical"), retain=True)
        client.publish("yamaha/input/analog/state", str(yam1.input_source_name == "Analog"), retain=True)
        published.input_source = yam1.input_source
    if published.mute != yam1.mute: 
        client.publish("yamaha/mute", yam1.mute, retain=True)
        published.mute = yam1.mute
    if published.volume != yam1.volume: 
        client.publish("yamaha/volume", yam1.volume, retain=True)
        published.volume = yam1.volume
    if published.sub != yam1.sub: 
        client.publish("yamaha/sub", yam1.sub, retain=True)
        published.sub = yam1.sub
    if published.surround != yam1.surround: 
        client.publish("yamaha/surround", yam1.surround, retain=True)
        client.publish("yamaha/style/surround/state", yam1.surround, retain=True)
        published.surround = yam1.surround
    if published.style != yam1.style: 
        client.publish("yamaha/style", yam1.style_name, retain=True)
        client.publish("yamaha/style/movie/state", str(yam1.style_name == "Movie"))
        client.publish("yamaha/style/game/state", str(yam1.style_name == "Game"))
        client.publish("yamaha/style/standard/state", str(yam1.style_name == "Standard"))
        published.style = yam1.style
    if published.clear_voice != yam1.clear_voice: 
        client.publish("yamaha/clear_voice", yam1.clear_voice, retain=True)
        published.clear_voice = yam1.clear_voice
    if published.bass != yam1.bass: 
        client.publish("yamaha/bass", yam1.bass, retain=True)
        published.bass = yam1.bass
    if published.leds != yam1.leds: 
        client.publish("yamaha/led", yam1.leds_name, retain=True)
        client.publish("yamaha/led/off/state", str(yam1.leds_name== "Off"), retain=True)
        client.publish("yamaha/led/dim/state", str(yam1.leds_name== "Dim"), retain=True)
        client.publish("yamaha/led/bright/state", str(yam1.leds_name== "Bright"), retain=True)
        published.leds = yam1.leds

def main_mqtt(pill2kill):
    while not pill2kill.is_set():
        try:
            logger.info("MQTT Started")
            mqtt.Client.connected_flag=False
            client = mqtt.Client('soundbar')
            client.on_connect=on_connect
            client.on_message=on_message
            client.username_pw_set(username=MQTT_UNAME,password=MQTT_PASSWORD)
            client.loop_start()
            client.connect(MQTT_IP)
            while not client.connected_flag: #wait in loop
                logger.debug("In wait loop")
                time.sleep(0.1)
            client.subscribe("yamaha/mute/switch")
            client.subscribe("yamaha/power/switch")
            client.subscribe("yamaha/input/switch")
            client.subscribe("yamaha/volume/switch")
            client.subscribe("yamaha/vol_up/switch")
            client.subscribe("yamaha/vol_down/switch")
            client.subscribe("yamaha/sub_up/switch")
            client.subscribe("yamaha/sub_down/switch")
            client.subscribe("yamaha/surround/switch")
            client.subscribe("yamaha/style/switch")
            client.subscribe("yamaha/style/game")
            client.subscribe("yamaha/style/movie")
            client.subscribe("yamaha/style/standard")
            client.subscribe("yamaha/style/surround")
            client.subscribe("yamaha/clear_voice/switch")
            client.subscribe("yamaha/bass/switch")
            client.subscribe("yamaha/led/switch")
            client.subscribe("yamaha/led/off")
            client.subscribe("yamaha/led/dim")
            client.subscribe("yamaha/led/bright")
            client.subscribe("yamaha/input/tv")
            client.subscribe("yamaha/input/bluetooth")
            client.subscribe("yamaha/input/optical")
            client.subscribe("yamaha/input/analog")
            while not pill2kill.is_set():
                publisher(client)
                time.sleep(0.1)
            client.loop_stop()
            client.disconnect()
        except Exception as e:
            logger.error("MQTT error raised: " + str(e))
            logger.exception(e)
        finally:
            logger.warning("MQTT has shutdown")
