from werkzeug import security 
from . import db


# Models for authentication

class User(db.Model):
    """
    Model of the user for authentication
    """
    __tablename__ = 'user'

    email = db.Column(db.String, primary_key=True, unique=True)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    institute = db.Column(db.String)
    category = db.Column(db.String)     # administrator, physicist, technologist, nurse, physician)
    
    password_hash = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """
        Retun True if the user is active
        """
        return True

    def get_id(self):
        """
        Return the email to satisfy Flask-Login's requirements
        """
        return self.email

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
            
    def generate_password_hash(self, password):
        return security.generate_password_hash(password)

    def check_password_hash(self, password):
        return security.check_password_hash(self.password_hash, password)

    @property
    def __repr__(self):
        return '<User {0}>'.format(self.email)


# Models for storage data about the process

status_verb = ['TIMED-OUT', 'ABORTED', 'ERROR', 'UNKNOWN',
               'PENDING', 'COPY-PENDING', 'PROCESSING', 'SUCCESS']


class Project(db.Model):
    __tablename__ = 'project'
    
    project_ID = db.Column(db.Integer, primary_key=True)
    project_path = db.Column(db.String, unique=False)
    project_filename = db.Column(db.String, unique=False)
    project_type = db.Column(db.String, unique=False)
    
    @property
    def __repr__(self):
        return '<Project {0}>'.format(self.project_ID)


class Patient(db.Model):
    __tablename__ = 'patient'
    
    patient_ID = db.Column(db.Integer, primary_key=True)
    patient_ID2 = db.Column(db.String, unique=True)
    patient_fname = db.Column(db.String, unique=False)
    patient_lname = db.Column(db.String, unique=False)
    patient_sex = db.Column(db.String, unique=False)
    patient_birth = db.Column(db.String, unique=False)
    patient_address1 = db.Column(db.String, unique=False)
    patient_address2 = db.Column(db.String, unique=False)

    def __repr__(self):
        return '<Patient {0}: {1} {2}>'.format(self.patient_ID, self.patient_fname, self.patient_lname)


class Job(db.Model):
    __tablename__ = 'job'
    
    job_ID = db.Column(db.Integer, primary_key=True)
    job_date = db.Column(db.String, unique=False)
    job_time = db.Column(db.String, unique=False)
    study_uid = db.Column(db.String, unique=False)
    plan_uid = db.Column(db.String, unique=False)
    fx_uid_low = db.Column(db.Integer, unique=False)
    fx_uid_hi = db.Column(db.Integer, unique=False)
    plan_name = db.Column(db.String, unique=False)
    macro_name = db.Column(db.String, unique=False)
    FractionNo = db.Column(db.Integer, unique=False)
    job_status = db.Column(db.Integer, unique=False)
    deliverable = db.Column(db.Integer, unique=False)
    priority = db.Column(db.Integer, unique=False)
    proc_date = db.Column(db.String, unique=False)
    proc_time = db.Column(db.String, unique=False)
    presc_dose = db.Column(db.Integer, unique=False)
    presc_fx = db.Column(db.Integer, unique=False)
    facility = db.Column(db.String, unique=False)
    machine = db.Column(db.String, unique=False)
    
    job_patient_ID = db.Column(db.Integer, db.ForeignKey('patient.patient_ID'))
    project_ID = db.Column(db.Integer, db.ForeignKey('project.project_ID'))
    
    patient = db.relationship('Patient', backref='job', lazy=True)
    project = db.relationship('Project', backref='job', lazy=True)

    def __repr__(self):
        return '<Job {0}>'.format(self.job_ID)


class Tolerance(db.Model):
    __tablename__ = 'tolerance'
    
    tolerance_ID = db.Column(db.Integer, primary_key=True)
    units = db.Column(db.String, unique=False)
    fail_low = db.Column(db.Float, unique=False)
    fail_hi = db.Column(db.Float, unique=False)
    warn_low = db.Column(db.Float, unique=False)
    warn_hi = db.Column(db.Float, unique=False)
    
    def __repr__(self):
        return 'Tolerance <{0}>'.format(self.tolerance_ID)
          

class Constrain(db.Model):
    __tablename__ = 'constrain'
    
    constrain_ID = db.Column(db.Integer, primary_key=True)
    region_id = db.Column(db.Integer, unique=False)
    region_type = db.Column(db.String, unique=False)
    region_name = db.Column(db.String, unique=False)
    dose = db.Column(db.Float, unique=False)
    volume = db.Column(db.Float, unique=False)
    calculated_value = db.Column(db.Float, unique=False)
    
    constrain_job_ID = db.Column(db.Integer, db.ForeignKey('job.job_ID'))
    tolerance_id = db.Column(db.Integer, db.ForeignKey('tolerance.tolerance_ID'))
    
    job = db.relationship('Job', backref='constrain', lazy=True)
    tolerance = db.relationship('Tolerance', backref='constrain', lazy=True)
    
    def __repr__(self):
        return 'Constrain <{0}>'.format(self.constrain_ID)
        
        
class Gamma(db.Model):
    __tablename__ = 'gamma'
    
    gamma_ID = db.Column(db.Integer, primary_key=True)
    region_id = db.Column(db.Integer, unique=False)
    region_type = db.Column(db.String, unique=False)
    region_name = db.Column(db.String, unique=False)
    dta = db.Column(db.Float, unique=False)
    dose_dif = db.Column(db.Float, unique=False)
    total_points = db.Column(db.Integer, unique=False)
    pass_points = db.Column(db.Integer, unique=False)
    fail_points = db.Column(db.Integer, unique=False)
    
    gamma_job_ID = db.Column(db.Integer, db.ForeignKey('job.job_ID'))
    tolerance_id = db.Column(db.Integer, db.ForeignKey('tolerance.tolerance_ID'))
    
    job = db.relationship('Job', backref='gamma', lazy=True)
    tolerance = db.relationship('Tolerance', backref='gamma', lazy=True)
    
    def __repr__(self):
        return '<Gamma {0}>'.format(self.gamma_ID)
        
               
class Poa(db.Model):
    __tablename__ = 'poa'
    
    poa_ID = db.Column(db.Integer, primary_key=True)
    region_id = db.Column(db.Integer, unique=False)
    region_type = db.Column(db.String, unique=False)
    region_name = db.Column(db.String, unique=False)
    poa_value = db.Column(db.Float, unique=False)
    
    poa_job_ID = db.Column(db.Integer, db.ForeignKey('job.job_ID'))
    tolerance_id = db.Column(db.Integer, db.ForeignKey('tolerance.tolerance_ID'))
    
    job = db.relationship('Job', backref='poa', lazy=True)
    tolerance = db.relationship('Tolerance', backref='poa', lazy=True)
    
    def __repr__(self):
        return '<Poa {0}>'.format(self.poa_ID)
