import json
import flask 
import flask_login 

from primo_website import controller
from primo_website import login_manager


mod = flask.Blueprint('general', __name__)

@mod.route('/', methods=['GET'])
def index():
    return flask.render_template('index.html')


@mod.route("/login", methods=["GET", "POST"])
def login():
    """
    For GET requests, display the login form
    For POST, login the current user by processing the form
    """
    if flask.request.method == 'POST':
        data = json.loads(flask.request.values['data'])
        if controller.login(data.username, data.password):
            return flask.redirect(flask.url_for("mod.jobs"))  
    return flask.render_template("login.html")


@mod.route('/jobs', methods=['GET'])
@flask_login.login_required
def jobs():
    jobs, verbose = controller.get_jobs_by_patient()
    return flask.render_template('jobs.html', jobs=jobs, verbose=verbose)
