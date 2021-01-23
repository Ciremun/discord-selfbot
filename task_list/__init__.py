from flask import Flask

def create_app():
    app = Flask(__name__)
    from . import task_list
    app.register_blueprint(task_list.bp)
    return app