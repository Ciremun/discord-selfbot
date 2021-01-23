import asyncio
from threading import Thread

from flask import Flask

async def run_client(loop):
    client.run(os.environ.get('DISCORD_TOKEN'), bot=src.config.bot, loop=loop)

def main():
    import os
    from os.path import join, dirname
    from dotenv import load_dotenv

    import src.config
    import src.commands
    from src.client import client

    load_dotenv(join(dirname(__file__), '.env'))

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(run_client(loop))

def create_app():
    app = Flask(__name__)

    from . import task_list

    app.register_blueprint(task_list.bp)

    selfbot_thread = Thread(target=main, daemon=True)
    selfbot_thread.start()

    return app