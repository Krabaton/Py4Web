from sqlalchemy import create_engine

import configparser


config = configparser.ConfigParser()
config.read('config.ini')

# URI

# engine = create_engine('postgresql://postgres:567234@localhost:5432/postgres', echo=True, pool_size=10)

user = config.get('DB', 'user')
password = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

engine = create_engine(f'postgresql://{user}:{password}@{domain}:5432/{db_name}', echo=True, pool_size=5)
