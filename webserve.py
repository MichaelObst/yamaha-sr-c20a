#called from main as a thread to run the web server

from config import *
from flask import Flask, json, request, cli
import logging

logger = logging.getLogger(__name__)

cli.show_server_banner = lambda *_: None

api = Flask(__name__)

@api.route('/status', methods=['GET'])
def get_status():
    return yam1.html()

@api.route('/do/<button>', methods=['GET'])
def do_button(button):
    argvol = request.args.get('vol', default = None, type = str)
    if argvol != None:
        try:
            if int(argvol) >= 0 & int(argvol) <= 255:
                command_queue.put(['volumeSet', int(argvol)])
            else:
                logger.warning("Vol set to invalid value")
        except ValueError:
            logger.warning("Vol set to not an integer")
    else:
        command_queue.put([button])
    return button + " : " + str(argvol), 201

def start_server(pill2kill):
    logger.info("Web Server starting")
    api.run(host=WEB_HOST_NAME, port=WEBPORT, debug=False, use_reloader=False)
    loger.error("Web Server has encountered an error and is no longer running")
