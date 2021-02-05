import os
import sys
import pathlib

PROJECT_BASE_PATH = os.path.dirname(__file__)
PROJECT_BASE_PATH = os.path.dirname(PROJECT_BASE_PATH)
LOG_DIR = os.path.join(PROJECT_BASE_PATH, 'logs')
sys.path.append(PROJECT_BASE_PATH)
pathlib.Path(LOG_DIR).mkdir(exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, "blue-bot.log")
LOG_FORMAT = f'%(pathname)s:%(lineno)d %(levelname)s - %(message)s'

# MONGO_SETTINGS
MONGO_HOST = "mongodb"
MONGO_PORT = 27017
MONGO_DEFAULT_DATABASE = "BLUE-BOT-DB"
MONGO_USERNAME = ''
MONGO_PASSWORD = ''
USER_DATA_COLLECTION = 'user-data'


# DISCORD SETTINGS
DISCORD_TOKEN = 'ODA3MTQ2NDA4MTQxNjUxOTc4.YBzvqw.l_Et03sG2UyVBd7IodJ0bMnVMKI'
DISCORD_GUILD = "kanak's server"
