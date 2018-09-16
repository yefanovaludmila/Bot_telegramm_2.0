''' Run file '''
import argparse
from flask import Flask


import telepot
from telepot.loop import MessageLoop
from utils import Utils
from view import View
from db_file import DbRunner

APP = Flask(__name__)

PARSER = argparse.ArgumentParser(description='Some initial bot.')
PARSER.add_argument('--config',
                    type=str,
                    help='A config fole with required params',
                    required=True)
ARGS = PARSER.parse_args()

UTI = Utils(ARGS.config)

LOGGER = UTI.get_logger()

TOKEN = UTI.get_token()

BOT = telepot.Bot(TOKEN)
DB = DbRunner()
VIWER = View(BOT, DB, LOGGER)

MessageLoop(BOT, VIWER.root_handle).run_as_thread()
print('I am ready to work ...')

if __name__ == '__main__':
    APP.run()
