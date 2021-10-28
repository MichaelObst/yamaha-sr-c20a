from config import *
import pygatt
import time
import logging
import traceback

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
        logger.warning("Received empty data packet")
    else:
        logger.warning("Received data that is not an expected message size: 0x%s" % (value.hex()))
    if (handle != RECEIVE_HANDLE): logger.warning("Bad handle: %s" % str(handle))

def BleServer(pill2kill):
    while not pill2kill.is_set():
        logger.info("Starting BLE")
        adapter = pygatt.GATTToolBackend()
        try:
            adapter.start(reset_on_start=False) #Setting to True requires sudo but may be more stable
            device = adapter.connect(DEVICEADDR, timeout=5.0)
            device.subscribe(UUID, callback=handle_data)
            time.sleep(1)
            command = send_command(['request'], yam1) #do an initial Req/Ack
            device.char_write_handle(STANDARD_HANDLE, command, wait_for_response=False)
            lastreq = time.time()
            while not pill2kill.is_set():
                if command_queue.empty() and (time.time() - lastreq) > 1:
                    logger.debug("Send Status Request")
                    command = send_command(['request'], yam1)
                    lastreq = time.time()
                    device.char_write_handle(STANDARD_HANDLE, command, wait_for_response=False)
                elif not command_queue.empty():
                    command_from_queue = command_queue.get()
                    command = send_command(command_from_queue, yam1)
                    logger.info("Sent: " + str(command_from_queue) + " 0x" + str(command.hex()))
                    device.char_write_handle(STANDARD_HANDLE, command, wait_for_response=False)
                    lastreq -= 1
        except Exception as e:
            logger.error('Some BLE Error: ' + str(e))
            logger.exception(e)
        finally:
            logger.warning('Stopping BLE')
            adapter.stop()
        logger.warning('BLE stopped')



