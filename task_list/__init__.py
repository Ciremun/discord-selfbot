import asyncio
from threading import Thread

from flask import Flask

def main():
    import os
    from os.path import join, dirname
    from dotenv import load_dotenv

    import src.config
    import src.commands
    from src.client import client

    load_dotenv(join(dirname(__file__), '.env'))

    loop = asyncio.new_event_loop()

    client.run(os.environ.get('DISCORD_TOKEN'), bot=src.config.bot, loop=loop)

def create_app():
    app = Flask(__name__)

    from . import task_list

    app.register_blueprint(task_list.bp)

    selfbot_thread = Thread(target=main, daemon=True)
    selfbot_thread.start()

    return app