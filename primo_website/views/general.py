import flask 
from primo_website import controller

mod = flask.Blueprint('general', __name__)

@mod.route('/', methods=['GET'])
def index():
    return flask.render_template('index.html')

@mod.route('/jobs', methods=['GET'])
def jobs():
    jobs, verbose = controller.get_jobs_by_patient()
    return flask.render_template('jobs.html', jobs=jobs, verbose=verbose)
