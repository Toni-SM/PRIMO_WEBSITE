import json
import flask 
import flask_login 
from flask import current_app

from primo_website import controller
from primo_website import login_manager


mod = flask.Blueprint('general', __name__)

@mod.route('/', methods=['GET'])
@mod.route('/index', methods=['GET'])
def index():
    return flask.render_template('index.html')


@mod.route("/login", methods=["GET", "POST"])
def login():
    """
    For GET requests, display the login form
    For POST, login the current user by processing the form
    """
    # POST request
    if flask.request.method == 'POST':
        data = json.loads(flask.request.values['data'])
        response = {"status": False, "message": "Wrong user or password"}
        # ckeck the username and password
        if controller.login(data["username"], data["password"]):
            response["status"]=True
            response["message"]=""
            return flask.jsonify(response)
        return flask.jsonify(response)
    # GET request
    return flask.render_template("login.html")


@mod.route("/logout", methods=["GET", "POST"])
def logout():
    controller.logout()
    return flask.redirect(flask.url_for('general.index'))

# jobs 

@mod.route('/jobs', methods=['GET'])
@flask_login.login_required
def jobs():
    _jobs, _verbose = controller.get_jobs_by_patient()
    return flask.render_template('jobs.html', jobs=_jobs, verbose=_verbose)

@mod.route('/job/<path:id>', methods=['GET'])
@flask_login.login_required
def job(id):
    _job, _gamma, _poa, _patient = controller.get_job(id)
    return flask.render_template('job.html', job=_job, gamma=_gamma, poa=_poa, patient=_patient)
    
@mod.route('/download-job-pdf/<path:id>')
@flask_login.login_required
def download_job_pdf(id):
    # TODO: build the real job's details pdf download path
    filename=controller.get_job_pdf(id)
    return flask.send_from_directory(current_app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# patients
    
@mod.route('/patients', methods=['GET'])
@flask_login.login_required
def patients():
    _patients = controller.get_patients()
    return flask.render_template('patients.html', patients=_patients)
    
@mod.route('/patient/<path:id>', methods=['GET'])
@flask_login.login_required
def patient(id):
    _patient, _jobs, _verbose = controller.get_patient(id)
    return flask.render_template('patient.html', patient=_patient, jobs=_jobs, verbose=_verbose)
