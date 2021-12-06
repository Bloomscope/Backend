from .. import db, model, create_app as app
from datetime import date, datetime
from sqlalchemy import func
from flask import Blueprint, current_app
from apscheduler.schedulers.background import BackgroundScheduler


job = Blueprint('job', __name__)


def activate_test():
    with app().app_context():
        print('running')
        tests = model.Test.query.filter(func.DATE(model.Test.conducted_on) == date.today()).all()
        for i in tests:
            if i.conducted_on <= datetime.now() and not i.is_active:
                i.is_active = True
        db.session.commit()


def deactivate_test():
    with app().app_context():
        tests = model.Test.query.filter(func.DATE(model.Test.conducted_on) == date.today()).all()
        for i in tests:
            if i.ends_on >= datetime.now() and i.is_active:
                i.is_active = False
        db.session.commit()


@job.before_app_first_request
def initialize():
    # print('here hitteddd')
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.start()
    scheduler.add_job(activate_test ,'interval', minutes=1)
    scheduler.add_job(deactivate_test ,'interval', minutes=1)