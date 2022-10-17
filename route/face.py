from flask import Blueprint

face = Blueprint('face', __name__, url_prefix='/face')

@face.route('/upload')
def upload():
    return 'upload'
