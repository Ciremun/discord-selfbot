from flask import Blueprint

bp = Blueprint('task_list', __name__)


@bp.route('/')
def index():
    return 'this app wuns my <a href="https://github.com/Ciremun/discord-selfbot" style="color: #ff69b4">discowd sewfbot</a> owo'