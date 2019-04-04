from . import db

status_verb = ['TIMED-OUT', 'ABORTED', 'ERROR', 'UNKNOWN',
               'PENDING', 'COPY-PENDING', 'PROCESSING', 'SUCCESS']

class Patient(db.Model):
    __tablename__ = 'patient'
    
    patient_id = db.Column(db.Integer, primary_key=True)
    patient_id2 = db.Column(db.String(25), unique=True)
    patient_fname = db.Column(db.String(25), unique=False)
    patient_lname = db.Column(db.String(25), unique=False)
    patient_sex = db.Column(db.String(6), unique=False)
    patient_birth = db.Column(db.String(8), unique=False)
    patient_address1 = db.Column(db.String(45), unique=False)
    patient_address2 = db.Column(db.String(45), unique=False)

    @property
    def __repr__(self):
        return '<%r>' % self.patient_lname

class Job(db.Model):
    __tablename__ = 'job'
    
    job_id = db.Column(db.Integer, primary_key=True)
    job_date = db.Column(db.String(15), unique=False)
    job_time = db.Column(db.String(15), unique=False)
    # project_id = db.Column(db.Integer, db.ForeingKey('project.project_id'))
    project_id = db.Column(db.Integer, unique=True)
    study_uid = db.Column(db.String(62), unique=False)
    plan_uid = db.Column(db.String(62), unique=False)
    fx_uid_low = db.Column(db.Integer, unique=False)
    fx_uid_hi = db.Column(db.Integer, unique=False)
    plan_name = db.Column(db.String(45), unique=False)
    macro_name = db.Column(db.String(45), unique=False)
    fractionNo = db.Column(db.Integer, unique=False)
    job_status = db.Column(db.Integer, unique=False)
    deliverable = db.Column(db.Integer, unique=False)
    priority = db.Column(db.Integer, unique=False)
    facility = db.Column(db.String(25), unique=False)
    machine = db.Column(db.String(25), unique=False)
    
    job_patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'))
    patient = db.relationship('Patient', backref='job', lazy=True)

    @property
    def __repr__(self):
        return '<%r>' % self.plan_name
