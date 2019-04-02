import flask 

mod = flask.Blueprint('general', __name__)

@mod.route('/', methods=['GET'])
def index():
    return flask.render_template('index.html')
