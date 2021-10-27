import time
import logging
from functions import *

logger = logging.getLogger(__name__)

class yam:
    LED_val = ["Bright", "Dim", "Off"]
    Style_val = ["NA", "NA", "NA", "Movie", "NA", "NA", "NA", "NA", "NA", "NA", "Standard", "NA", "Game"]
    Input_val = ["NA", "NA", "NA", "NA", "NA", "Bluetooth", "NA", "TV", "NA", "NA", "Optical", "NA", "Analog"]

    def __init__(self):
        self.state = "uninit"
        self.power = None
        self.input_source = None
        self.input_source_name = None
        self.mute = None
        self.volume = None
        self.sub = None
        self.surround = None
        self.style = None
        self.style_name = None
        self.clear_voice = None
        self.bass = None
        self.leds = None
        self.leds_name = None
        self.time = time.time()

    def set_by_hex(self, data): #send in the full data
            #can assume length for this one is 
            logger.debug(hex(data))
            if (data >> 104 != 0xccaa0e0500):
                logger.warning("Missing expected 0xccaa0e0500 at start of data")
            if (data >> 40) & 16777215 != 0x202000:
                logger.warning("Missing expected 0x202000 in data")
            cleaned_data = data & (0x10 ** 32 - 1) #strip 0xCCAA given fixed length
            if not checksum_int(cleaned_data):
                logger.warning("Bad checksum in data")
            self.state = "init"
            self.power = bool((data >> 96) & 1)
            self.input_source = (data >> 88) & 0xff
            self.input_source_name = self.Input_val[self.input_source]
            self.mute  = bool((data >> 80) & 1)
            self.volume = (data >> 72) & 0xff
            self.sub   = (data >> 64) & 0xff
            self.surround = bool((data >> 32) & 1)
            self.style = (data >> 24) & 0xff
            self.style_name = self.Style_val[self.style]
            self.clear_voice = bool((data >> 18) & 1)
            self.bass = bool((data >> 21) & 1)
            self.leds = (data >> 8) & 0x3
            self.leds_name = self.LED_val[self.leds]
            self.time = time.time()

    def string(self):
        out = ("Power:   " + str(self.power)) + \
        ("\r\nInput:   " + yam.Input_val[self.input_source]) + \
        ("\r\nMute:    " + str(self.mute)) + \
        ("\r\nVolume:  " + str(self.volume)) + \
        ("\r\nSub Vol: " + str(self.sub)) + \
        ("\r\nSurround:" + str(self.surround)) + \
        ("\r\nStyle:   " + yam.Style_val[self.style]) + \
        ("\r\nVoice:   " + str(self.clear_voice)) + \
        ("\r\nBass:    " + str(self.bass)) + \
        ("\r\nLEDs:    " + yam.LED_val[self.leds]) + \
        ("\r\nTime:    " + str(self.time))
        return out

    def html(self):
        return self.string().replace("\r\n", "<br>")


