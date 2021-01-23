import os
from os.path import join, dirname
from dotenv import load_dotenv

import src.config
import src.commands
from src.client import client


if __name__ == '__main__':
    print('run pepega')
    load_dotenv(join(dirname(__name__), '.env'))
    client.run(os.environ.get('DISCORD_TOKEN'), bot=src.config.bot)