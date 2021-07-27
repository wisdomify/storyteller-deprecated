import os
from dotenv import load_dotenv, find_dotenv

from storyteller.collect.utils.DBConnector import DBController

load_dotenv(find_dotenv())

OPENDICT_API_KEY = os.getenv('opendict_api')

GW_USER = os.getenv('gw_username')
GW_HOST = os.getenv('gw_host')
GW_PKEY = os.getenv('gw_pkey')
GW_PORT = int(os.getenv('gw_port'))

DB_USER = os.getenv('db_username')
DB_HOST = os.getenv('db_host')
DB_PW = os.getenv('db_password')
DB_PORT = int(os.getenv('db_port'))

STORYTELLER_SCHEMA = os.getenv('storyteller_schema')

controller = DBController(user=DB_USER,
                          password=DB_PW,
                          schema=STORYTELLER_SCHEMA)
