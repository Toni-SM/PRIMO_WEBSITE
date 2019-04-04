from flask import session
from primo_website import db, model

def get_jobs_by_patient():
    jobs = db.session.query(model.Job).join(model.Patient).filter(model.Patient.patient_id == model.Job.job_patient_id)
    if jobs is None:
        return []
    for jb in jobs:
      jb.job_status += 3

    return jobs, model.status_verb