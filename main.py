import os
from os.path import join, dirname

from dotenv import load_dotenv

import src.config
import src.commands
from src.client import client


if __name__ == '__main__':
    load_dotenv(join(dirname(__name__), '.env'))
    client.run(os.environ.get('DISCORD_SELFBOT_TOKEN'), bot=src.config.bot)