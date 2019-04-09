from werkzeug import security 

from . import db_login as db

class User(db.Model):
    """
    :param username: username or email of user
    :type username: srt
    :param password: encrypted password of user
    :type password: srt
    """
    __tablename__ = 'user'

    username = db.Column(db.String, primary_key=True)
    password_hash = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """
        Retun True if the user is active
        """
        return True

    def get_id(self):
        """
        Return the username to satisfy Flask-Login's requirements
        """
        return self.username

    def is_authenticated(self):
        """
        Return True if the user is authenticated
        """
        return self.authenticated

    def is_anonymous(self):
        """
        False, as anonymous users aren't supported
        """
        return False
        
    
    def set_password(self, password):
        self.password_hash = security.generate_password_hash(password)

    def check_password(self, password):
        return security.check_password_hash(self.password_hash, password)



    @property
    def __repr__(self):
        return '<%r>' % self.patient_lname
