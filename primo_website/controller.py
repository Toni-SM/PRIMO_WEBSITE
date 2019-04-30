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
    :return: the status of the registration
    :type: bool
    """
    print(data)
    print(type(data))
    
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

def accounts():
    users = db.session.query(model.User)
    return users
    
def get_jobs_by_patient():
    jobs = db.session.query(model.Job).join(model.Patient).filter(model.Patient.patient_id == model.Job.job_patient_id)
    if jobs is None:
        return []
    for jb in jobs:
      jb.job_status += 3

    return jobs, model.status_verb
