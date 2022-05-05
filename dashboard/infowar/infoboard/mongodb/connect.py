import configparser
from pymongo import MongoClient
from pathlib import Path
from django.conf import settings

filename = Path(settings.BASE_DIR / 'config.ini')
config = configparser.ConfigParser()
config.read(filename)

user = config.get('DB', 'user')
password = config.get('DB', 'pass')

client = MongoClient(f'mongodb+srv://{user}:{password}@cluster0.smeju.mongodb.net/?retryWrites=true&w=majority')

db = client['infowar']