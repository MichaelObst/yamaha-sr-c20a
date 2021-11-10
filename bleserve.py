from config import *
import time
import logging
import traceback
import asyncio
import bleak

logger = logging.getLogger(__name__)


def handle_data(handle, value):
    """
    handle -- integer, characteristic read handle the data was received on
    value -- bytearray, the data returned in the notification
    """
    logger.debug("Received data: %s" % (value.hex()))
    if (len(value) > 3):
        length = value[2]
        if (value[0] != 0xcc):
            logger.warning("Bad first bit: 0x%s" % (value.hex()))
        elif (value[1] != 0xaa):
            logger.warning("Bad second bit: 0x%s" % (value.hex()))
        elif not checksum_byte(value):
            logger.warning("Bad checksum in data: 0x%s" % (value.hex()))
        elif (len(value) - 4 != length):
            logger.warning("Bad value for data length: 0x%s" % (value.hex()))
        else:
            
            if (length == 14): #this should be a status message
                yam1.set_by_hex(int(value.hex(), 16))
                logger.debug(yam1.string())
            elif (length == 2):
                logger.info("Received: " + interpret_message(value))
            elif (length == 3):
                logger.info("Received: " + interpret_message(value))
            elif (length == 5):
                logger.info("Received: " + interpret_message(value))
            else:
                logger.warning("Received unexpected data length: 0x%s" % (value.hex()))
    elif value.hex() == "":
        logger.warning("Received empty data packet, this is expected once on startup")
    else:
        logger.warning("Received data that is not an expected message size: 0x%s" % (value.hex()))
    if (handle != RECEIVE_HANDLE): logger.warning("Bad handle: %s" % str(handle))

async def BleServer(pill2kill):
    logger.info("Starting BLE")
    adapter = bleak.BleakClient(DEVICEADDR)
    try:
        scanner = bleak.BleakScanner() #### DON'T know why but must be scanning at the time we connect.... Weirdness
        await scanner.start()
        await adapter.connect()
        await scanner.stop()
        await adapter.start_notify(UUID, handle_data)
        #time.sleep(1)
        command = send_command(['request'], yam1) #do an initial Req/Ack
        await adapter.write_gatt_char(STANDARD_HANDLE, command)
        lastreq = time.time()
        while not pill2kill.is_set():
            if command_queue.empty() and (time.time() - lastreq) > 3:
                logger.info("loop")
                logger.debug("Send Status Request")
                command = send_command(['request'], yam1)
                lastreq = time.time()
                await adapter.write_gatt_char(STANDARD_HANDLE, command)
            elif not command_queue.empty():
                command_from_queue = command_queue.get()
                command = send_command(command_from_queue, yam1)
                logger.info("Sent: " + str(command_from_queue) + " 0x" + str(command.hex()))
                await adapter.write_gatt_char(STANDARD_HANDLE, command)
                lastreq = 0
            await asyncio.sleep(0.1)
    except Exception as e:
        logger.error('Some BLE Error: ' + str(e))
        logger.exception(e)
    finally:
        logger.warning('Stopping BLE')
        await adapter.disconnect()
    logger.warning('BLE stopped')

def start_bleak(pill2kill):
    while not pill2kill.is_set():
        asyncio.run(BleServer(pill2kill))
    return
