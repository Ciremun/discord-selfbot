from threading import Thread
import os
from os.path import join, dirname

from flask import Flask

import src.config
import src.commands
from src.client import client, loop


def run_client():
    loop.create_task(client.start(os.environ.get('DISCORD_TOKEN'), bot=src.config.bot))
    Thread(target=loop.run_forever()).start()


def create_app():
    app = Flask(__name__)

    from . import task_list

    app.register_blueprint(task_list.bp)

    run_client()

    return app
