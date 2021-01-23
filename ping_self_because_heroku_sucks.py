import os
import time
from random import randrange
from os.path import join, dirname

import requests
from dotenv import load_dotenv

load_dotenv(join(dirname(__name__), '.env'))

self_url = os.environ.get('SELF_URL')

while True:
    time.sleep(randrange(8, 28) * 60)
    requests.get(self_url)