from flask import Blueprint, Response

bp = Blueprint('task_list', __name__)

@bp.route('/')
def index():
    return Response(200)