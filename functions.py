import logging

logger = logging.getLogger(__name__)

def checksum_int(input):
    #checks the checksum of the data as an int expects removal of 0xCCAA but keep length byte and checksum
    input = input.to_bytes(len(hex(input)), 'big')
    return checksum_byte(input)


def checksum_byte(input):
    #checks the checksum of the data as a byte array
    sum = 0
    for i in input[2:-1]:
        sum += i
    sum = ~ sum #invert
    sum = sum & 255 #take last 8 bits
    sum += 1
    if (sum != input[-1]):
        return False
    else:
        return True

def checksum_make(input):
    #creates a checksum from byte array and returns int
    sum = 0
    for i in input:
        sum += i
    sum = ~ sum #invert
    sum = sum & 255 #take last 8 bits
    sum += 1
    return sum

def send_command(command, yam1):
    #takes a list of arguments and returns bytes for that command, will return req if invalid.
    logger.debug(command)
    if len(command) == 1: #single action typ
        command = command[0]
        if command == 'handshake': data = bytearray([0x01,0x48,0x54,0x54,0x20,0x43,0x6f,0x6e,0x74])
        elif command == 'powerOn': data = bytearray([0x40,0x78,0x7e])
        elif command == 'powerOff': data = bytearray([0x40,0x78,0x7f])
        elif command == 'powerToggle':
            if yam1.power == True: return send_command(['powerOff'], yam1)
            else: return send_command(['powerOn'], yam1)
        elif command == 'inputBluetooth': data = bytearray([0x40,0x78,0x29])
        elif command == 'inputTV': data = bytearray([0x40,0x78,0xdf])
        elif command == 'inputOptical': data = bytearray([0x40,0x78,0x49])
        elif command == 'inputAnalog': data = bytearray([0x40,0x78,0xd1])
        elif command == 'subUp': data = bytearray([0x40,0x78,0x4c])
        elif command == 'subDown': data = bytearray([0x40,0x78,0x4d])
        elif command == 'muteOn': data = bytearray([0x40,0x7e,0xa2])
        elif command == 'muteOff': data = bytearray([0x40,0x7e,0xa3])
        elif command == 'muteToggle':
            if yam1.mute == True: return send_command(['muteOff'], yam1)
            else: return send_command(['muteOn'], yam1)
        elif command == 'volUp': return send_command(['volumeSet', min(int(yam1.volume) + 5, 60)], yam1)
        elif command == 'volDown': return send_command(['volumeSet', max(int(yam1.volume) - 5, 0)], yam1)
        elif command == 'standardMode': data = bytearray([0x40,0x7e,0xf1])
        elif command == 'surroundMode': data = bytearray([0x40,0x78,0x50])
        elif command == 'movieMode': data = bytearray([0x40,0x78,0xd9])
        elif command == 'gameMode': data = bytearray([0x40,0x78,0xdc])
        elif command == 'clearVoiceOn': data = bytearray([0x40,0x7e,0x80])
        elif command == 'clearVoiceOff': data = bytearray([0x40,0x7e,0x82])
        elif command == 'bassOn': data = bytearray([0x40,0x78,0x6e])
        elif command == 'bassOff': data = bytearray([0x40,0x78,0x6f])
        elif command == 'ledBright': data = bytearray([0x51,0x00])
        elif command == 'ledDim': data = bytearray([0x51,0x01])
        elif command == 'ledOff': data = bytearray([0x51,0x02])
        elif command == 'request': data = bytearray([0x03, 0x05])
        elif command == 'blue': data = bytearray([0x40, 0x78,0x34])
        elif command == 'dim': data = bytearray([0x40, 0x78,0xba])
        else:
            logger.warning("Invalid command sending req instead")
            data = bytearray([0x03, 0x05]) #Sends req instead
    elif len(command) == 2: #volume is the only time this is used that we know of
        if command[0] == 'volumeSet': data = bytearray([0x41, command[1]])
        else:
            logger.warning("Invalid command")
            data = bytearray([0x03, 0x05]) #Sends a req instead
    else:
            logger.warning("Bad command format, too long") #command was too long
            data = bytearray([0x03, 0x05]) #Sends a req instead
    data.insert(0, len(data))
    data.append(checksum_make(data))
    data.insert(0, 0xaa)
    data.insert(0, 0xcc)
    return bytes(data)

def interpret_message(val):
    #interprets a byte array message
    length = val[2]
    if length == 0x02:
        if val[3] == 0x10: #power
            if val[4] == 0x10: return "Power OFF"
            elif val[4] == 0x11: return "Power ON"
        elif val[3] == 0x11: #input
            if val[4] == 0x05: return "Input Bluetooth"
            if val[4] == 0x07: return "Input TV"
            if val[4] == 0x0A: return "Input Optical"
            if val[4] == 0x0C: return "Input Analog"
        elif val[3] == 0x13: #sub
            return "Subwoofer to: " + str(val[4])
        elif val[3] == 0x24: #led
            if val[4] == 0x02: return "LED Off"
            elif val[4] == 0x01: return "LED Dim"
            elif val[4] == 0x00: return "LED Bright"
    elif length == 0x03:
        if val[3] == 0x12:
            if val[4] == 0x01:
                return "Volume Message, Mute ON, volume: " + str(val[5])
            elif val[4] == 0x00:
                return "Volume Message, Mute OFF, volume: " + str(val[5])
    elif length == 0x05:
        if val[3] == 0x15: #style
            if val[4] != 0x00: "Unknown message: 0x" + (val.hex())

            if val[5] == 0x00:
                surround_string = "Off"
            elif val[5] == 0x01:
                surround_string = "On"
            else: "Unknown message: 0x" + (val.hex())

            if val[6] == 0x03: #movie
                style_string = "Movie"
            elif val[6] == 0x0c: #game
                style_string = "Game"
            elif val[6] == 0x0a: #standard
                style_string = "Standard"
            else: "Unknown message: 0x" + (val.hex())

            if val[7] == 0x00:
                voice_string = "Off"
                bass_string = "Off"
            elif val[7] == 0x20:
                voice_string = "Off"
                bass_string = "On"
            elif val[7] == 0x04:
                voice_string = "On"
                bass_string = "Off"
            elif val[7] == 0x24:
                voice_string = "On"
                bass_string = "On"
            else: "Unknown message: 0x" + (val.hex())
 
            return "Style Message, [Surround " + surround_string + "][Style " + style_string + "][Clear Voice " + voice_string + "][Bass Extension " + bass_string + "]"
    return "Unknown message: 0x" + (val.hex())
