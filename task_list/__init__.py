from threading import Thread

from flask import Flask

def main():
    import os
    from os.path import join, dirname

    import src.config
    import src.commands
    from src.client import client, loop

    loop.create_task(client.start(os.environ.get('DISCORD_TOKEN'), bot=src.config.bot))
    Thread(target=loop.run_forever()).start()

def create_app():
    app = Flask(__name__)

    from . import task_list

    app.register_blueprint(task_list.bp)

    Thread(target=main, daemon=True).start()

    return app