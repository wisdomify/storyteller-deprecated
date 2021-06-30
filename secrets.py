import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

OPENDICT_API_KEY = os.getenv('opendict_api')
