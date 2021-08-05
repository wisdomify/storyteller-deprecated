import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

OPENDICT_API_KEY = os.getenv('opendict_api')

DB_USER = os.getenv('db_username')
DB_HOST = os.getenv('db_host')
DB_PW = os.getenv('db_password')
DB_PORT = int(os.getenv('db_port'))

STORYTELLER_SCHEMA = os.getenv('storyteller_schema')
