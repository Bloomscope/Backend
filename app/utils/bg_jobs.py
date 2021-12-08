from .. import db, model, create_app as app
from datetime import date, datetime, timedelta
from sqlalchemy import func
from flask import Blueprint
from apscheduler.schedulers.background import BackgroundScheduler


job = Blueprint('job', __name__)
scheduler = BackgroundScheduler(daemon=True)


def activate_test():
    with app().app_context():
        tests = model.Test.query.filter(func.DATE(model.Test.conducted_on) == date.today()).all()
        for i in tests:
            if i.conducted_on <= datetime.now() and not i.is_active:
                i.is_active = True
        db.session.commit()


def deactivate_test():
    with app().app_context():
        tests = model.Test.query.filter(func.DATE(model.Test.conducted_on) == date.today()).all()
        for i in tests:
            if i.ends_on <= datetime.now() and i.is_active:
                i.is_active = False
        db.session.commit()


def schedule_test(test_id, starts_on, ends_on):
    with app().app_context():
        users = model.User.query.filter_by(user_type_id=1).all()
        for user in users:
            starts = user.registered_on + timedelta(starts_on)
            ends = user.registered_on + timedelta(ends_on)
            new_test = model.TestSchedule(starts_on=starts, ends_on=ends, test_id=test_id, user_id=user.id)
            db.session.add(new_test)
        db.session.commit()


def create_test(user_id, registered_on):
    with app().app_context():
        tests = model.Test.query.all()
        for test in tests:
            starts = registered_on + timedelta(test.conducted_on)
            ends = registered_on + timedelta(test.ends_on)
            new_test = model.TestSchedule(starts_on=starts, ends_on=ends, test_id=test.id, user_id=user_id)
            db.session.add(new_test)
        db.session.commit()


@job.before_app_first_request
def initialize():
    scheduler.start()
    scheduler.add_job(activate_test ,'interval', minutes=1)
    scheduler.add_job(deactivate_test ,'interval', minutes=1)