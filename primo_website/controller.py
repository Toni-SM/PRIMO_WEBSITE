from flask import session
import flask_login 

from primo_website import db, model
from primo_website import login_manager, db_login, model_login


@login_manager.user_loader
def load_user(user_id):
    """
    Given *user_id*, return the associated User object
    
    :param user_id: user_id (email) user to retrieve
    :type user_id: unicode
    """
    return model_login.User.get(user_id)

def login(username, password):
    """
    """
    user = model_login.User.query.get(username)
    if user:
        if user.check_password_hash(password):
            user.authenticated = True
            db_login.session.add(user)
            db_login.session.commit()
            flask_login.login_user(user, remember=True)
            return True
    return False
    
def logout():
    """
    Logout the current user
    """
    user = login_manager.current_user
    user.authenticated = False
    db_login.session.add(user)
    db_login.session.commit()
    flask_login.logout_user()
    return True




def get_jobs_by_patient():
    jobs = db.session.query(model.Job).join(model.Patient).filter(model.Patient.patient_id == model.Job.job_patient_id)
    if jobs is None:
        return []
    for jb in jobs:
      jb.job_status += 3

    return jobs, model.status_verb
