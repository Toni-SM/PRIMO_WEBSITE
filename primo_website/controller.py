from flask import session
import flask_login 
import sqlalchemy

from primo_website import db, model
from primo_website import login_manager

@login_manager.user_loader
def load_user(user_id):
    """
    Given *user_id*, return the associated User object
    
    :param user_id: user_id (username) user to retrieve
    :type user_id: unicode
    :return: retrieved User object or None
    :type: <class 'User'> or <class 'NoneType'>
    """
    return model.User.query.get(user_id)

def login(username, password):
    """
    Login the user if exist the username and password
    
    :param username: username of the user
    :type username: str
    :param password: password of the user
    :type password: str
    :return: the login status of the user
    :type: bool
    """
    user = model.User.query.get(username)
    if user:
        if user.check_password_hash(password):
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            flask_login.login_user(user, remember=True)
            return True
    return False
    
def logout():
    """
    Logout the current user
    
    :return: True if the logout was completed successfully
    :type: bool
    """
    try:
        user = flask_login.current_user
        user.authenticated = False
        db.session.add(user)
        db.session.commit()
        flask_login.logout_user()
    except Exception as e:
        print("logout", e)
        return False
    return True

def register(data):
    """
    Register the user if not exist
    
    :param data: data about the registration
    :type data: dict
    :return: the status of the registration and the error message
    :type: tuple(bool, str)
    """
    try:
        user = model.User(name=data["name"], 
                          surname=data["surname"], 
                          institute=data["institute"], 
                          category=data["category"], 
                          email=data["email"], 
                          password_hash=model.User.generate_password_hash(None, data["password"]))
        db.session.add(user)
        db.session.commit()        
        return True, ""
    except sqlalchemy.exc.IntegrityError:
        return False, "That account (email) is taken. Try another"
    except KeyError:
        return False, "The registration information was not properly provided to the server"
    except Exception as e:
        return False, "Internal server error: "+str(e)
    return False, ""

def remove(username):
    """
    Remove the user (if exist) given the username 
    """
    user = model.User.query.get(username)
    if user:
        db.session.delete(user)
        db.session.commit()  
        return True, ""
    return False, "That account (email) do not exist"
        
def accounts():
    """
    List the registered accounts order by name 
    
    :return: registered accounts
    :type: list
    """
    users = db.session.query(model.User).order_by(model.User.name).all()
    return users
    
    
def get_jobs_by_patient():
    jobs = db.session.query(model.Job).join(model.Patient).filter(model.Patient.patient_ID == model.Job.job_patient_ID).order_by(model.Patient.patient_ID2).all()
    if jobs is None:
        return []
    for jb in jobs:
      jb.job_status += 3

    return jobs, model.status_verb
    
def get_patients():
    patients = db.session.query(model.Patient).order_by(model.Patient.patient_lname).all()
    if patients is None:
        return []
    return patients

def get_patient(id):
    patient = db.session.query(model.Patient).filter(model.Patient.patient_ID == id).first()
    if patient is None:
        return []
    jobs = db.session.query(model.Job).filter(model.Job.job_patient_ID == id).order_by(model.Job.job_date).order_by(model.Job.job_time).all()
    if jobs is None:
        return []
    return patient, jobs, model.status_verb

def get_job(id):
    # job details
    job = db.session.query(model.Job).filter(model.Job.job_ID == id).first()
    if job is None:
        job = []
    # gamma analysis details
    gamma = db.session.query(model.Gamma).filter(model.Gamma.gamma_job_ID == id).join(model.Tolerance).filter(model.Tolerance.tolerance_ID == model.Gamma.tolerance_id).order_by(model.Gamma.region_name).all()
    if gamma is None:
        gamma = []
    # poa analysis details
    poa = db.session.query(model.Poa).filter(model.Poa.poa_job_ID == id).join(model.Tolerance).filter(model.Tolerance.tolerance_ID == model.Poa.tolerance_id).order_by(model.Poa.region_name).all()
    if poa is None:
        poa = []
    # patient details
    patient = []
    if job is not None:
        patient = db.session.query(model.Patient).filter(model.Patient.patient_ID == job.job_patient_ID).first()
    # validation
    validation = db.session.query(model.Validation).filter(model.Validation.validation_job_ID == id).join(model.User).order_by(model.User.name).all()
    if validation is None:
        validation = []
    return job, gamma, poa, patient, validation

def get_job_pdf(id):
    # TODO: get the real job's details pdf path
    return "test-pdf-document.pdf"

def job_validation(status, user_id, job_id):
    boolen_status = True if status == "validate" else False
    validation = db.session.query(model.Validation).filter(model.Validation.validation_job_ID == job_id).filter(model.Validation.validation_user_ID == user_id).first()    
    # remove validation
    if status == "remove":
        if validation is not None:
            db.session.delete(validation)
            db.session.commit()
            return True
    # insert or update
    else:
        if validation is None:
            validation = model.Validation(valid=boolen_status, validation_job_ID=job_id, validation_user_ID=user_id)
        else:
            validation.valid=boolen_status
        db.session.add(validation)
        db.session.commit()
        return True
    return False
    