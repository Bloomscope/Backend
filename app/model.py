import datetime
from . import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from .config import SECRET_KEY
from .dtypes import *
import uuid
from sqlalchemy import event
from .utils import bg_jobs


class UsersType(db.Model):
    ___tablename__ = 'users_type'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    type = db.Column(db.String(8), nullable=False) # student or user, teacher, admin
    access_level = db.Column(db.INTEGER, default=1) # 1 = user, 2 = teacher, 3 = admin
    users = db.relationship('User', backref='users_type', passive_deletes=True, lazy=True)


class Plans(db.Model):
    __tablename__ = 'plans'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    plan = db.Column(db.String(15), nullable=False, unique=True) # plan type. ex: gold for 3 months, etc
    validity = db.Column(db.INTEGER, nullable=False) # plan validity in days
    sub_ref = db.relationship('Subscription', backref='plans', lazy=True)


class Organization(db.Model):
    __tablename__ = 'organization'

    id = db.Column(GUID(), primary_key=True, default=lambda: str(uuid.uuid4()))
    added_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    name = db.Column(db.String(50), nullable=False)
    org_id = db.Column(db.String(8), unique=True, default=org_id().__str__())
    address = db.Column(db.String(50), nullable=False)
    registered_by = db.relationship('User', backref='organization', lazy=True)

    def as_dict(self):
        return {col.name: str(getattr(self, col.name)) for col in self.__table__.columns}


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(GUID(), primary_key=True, default=lambda: str(uuid.uuid4()))
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    fname = db.Column(db.String(20), nullable=False)
    mname = db.Column(db.String(20))
    lname = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    last_logged_in = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    is_verified = db.Column(db.Boolean, default=False)
    has_added_gaurdians = db.Column(db.Boolean, default=False)
    user_type_id = db.Column(db.INTEGER, db.ForeignKey('users_type.id', ondelete='CASCADE'), nullable=False, default=1) #make default to 1
    organization_id = db.Column(GUID(), db.ForeignKey('organization.id', ondelete='CASCADE'), default=None)
    subscription = db.relationship('Subscription', backref='user', lazy=True)
    parent_child_rel = db.relationship('Parent_Child', backref='user', lazy=True)
    q_added = db.relationship('Questions', backref='user', lazy=True)
    results = db.relationship('Results', backref='user', lazy=True)
    announcements = db.relationship('Announcements', backref='user', lazy=True)
    complains = db.relationship('Complain', backref='user', lazy=True)
    suggestions = db.relationship('Suggestions', backref='user', lazy=True)
    tokens = db.relationship('Token', backref='user', lazy=True)
    tests_tracker = db.relationship('TestSchedule', backref='user', lazy=True)

    def as_dict(self):
        return {col.name: str(getattr(self, col.name)) for col in self.__table__.columns}


class Subscription(db.Model):
    __tablename__ = 'subscription'

    id = db.Column(GUID(), primary_key=True, default=lambda: str(uuid.uuid4()))
    subscribed_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    expires_on = db.Column(db.DateTime, nullable=False)
    plan_id = db.Column(db.INTEGER, db.ForeignKey('plans.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(GUID(), db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)


class Parent(db.Model):
    __tablename__ = 'parent'

    id = db.Column(GUID(), primary_key=True, default=lambda: str(uuid.uuid4()))
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    fname = db.Column(db.String(20), nullable=False)
    mname = db.Column(db.String(20))
    lname = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    last_logged_in = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    user_type_id = db.Column(db.INTEGER, db.ForeignKey('users_type.id', ondelete='CASCADE'), nullable=False, default=2)
    parent_child_rel = db.relationship('Parent_Child', backref='parent', lazy=True)

    def as_dict(self):
        return {col.name: str(getattr(self, col.name)) for col in self.__table__.columns}


class Parent_Child(db.Model):
    __tablename__ = 'parent_child'

    parent_id = db.Column(GUID(), db.ForeignKey('parent.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    user_id = db.Column(GUID(), db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True, nullable=False)


class Parameters(db.Model):
    __tablename__ = 'parameters'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    param_name = db.Column(db.String(32), unique=True, nullable=False)
    mapped = db.relationship('Questions', backref='parameters', lazy=True)
    suggestions = db.relationship('Suggestions', backref='parameters', lazy=True)


class TestSchedule(db.Model):
    __tablename__ = 'testschedule'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    attempted_on = db.Column(db.DateTime, nullable=True)
    starts_on = db.Column(db.DateTime, nullable=True)
    ends_on = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=False)
    has_attempted = db.Column(db.Boolean, default=False)
    user_id = db.Column(GUID(), db.ForeignKey('user.id'), nullable=False)
    test_id = db.Column(GUID(), db.ForeignKey('test.id'), nullable=False)

    def as_dict(self):
        return {col.name: str(getattr(self, col.name)) for col in self.__table__.columns}


class Test(db.Model):
    __tablename__ = 'test'

    id = db.Column(GUID(), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(32), nullable=False, unique=True)
    conducted_on = db.Column(db.Integer, nullable=False)
    questions = db.Column(db.PickleType, nullable=True)
    durations = db.Column(db.INTEGER, nullable=False)
    ends_on = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    tracks = db.relationship('Questions', backref='test', lazy=True)
    res_tracks = db.relationship('Results', backref='test', lazy=True)
    tokens = db.relationship('Token', backref='test', lazy=True)
    test_schedules = db.relationship('TestSchedule', backref='test', lazy=True)

    def as_dict(self):
        return {col.name: str(getattr(self, col.name)) for col in self.__table__.columns}


class Questions(db.Model):
    __tablename__ = 'questions'

    id = db.Column(GUID(), primary_key=True, default=lambda: str(uuid.uuid4()))
    question = db.Column(db.PickleType, nullable=False)
    options = db.Column(db.PickleType, nullable=False)
    ans = db.Column(db.String(5), nullable=False)
    explanation = db.Column(db.Text)
    marks = db.Column(db.Integer, nullable=False)
    has_asked = db.Column(db.Boolean, default=False)
    param_id = db.Column(db.INTEGER, db.ForeignKey('parameters.id'), nullable=False)
    added_by_id = db.Column(GUID(), db.ForeignKey('user.id'), nullable=False)
    asked_on = db.Column(GUID(), db.ForeignKey('test.id'), default=None)

    def as_dict(self):
        data = {col.name: str(getattr(self, col.name)) for col in self.__table__.columns}
        del data['ans']
        del data['explanation']
        return data


class Results(db.Model):
    __tablename__ = 'results'

    id = db.Column(GUID(), primary_key=True, default=lambda: str(uuid.uuid4()))
    completed_on = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    test_id = db.Column(GUID(), db.ForeignKey('test.id'), nullable=False)
    # rename responses to result [store result resp here]
    responses = db.Column(db.PickleType, nullable=False)
    user_id = db.Column(GUID(), db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    def as_dict(self):
        return {col.name: str(getattr(self, col.name)) for col in self.__table__.columns}


class Announcements(db.Model):
    __tablename__ = 'announcements'

    id = db.Column(GUID(), primary_key=True, default=lambda: str(uuid.uuid4()))
    announced_on = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    announced_by = db.Column(GUID(), db.ForeignKey('user.id'), nullable=False)

    def as_dict(self):
        return {col.name: str(getattr(self, col.name)) for col in self.__table__.columns}


class Suggestions(db.Model):
    __tablename__ = 'suggestions'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    suggestion_name = db.Column(db.String(32), nullable=False, unique=True)
    param_id = db.Column(db.INTEGER, db.ForeignKey('parameters.id'), nullable=False)
    suggestion = db.Column(db.Text, nullable=False)
    student_id = db.Column(GUID(), db.ForeignKey('user.id'), nullable=False)

    def as_dict(self):
        return {col.name: str(getattr(self, col.name)) for col in self.__table__.columns}


class Complain(db.Model):
    __tablename__ = 'complain'

    id = db.Column(GUID(), primary_key=True, default=lambda: str(uuid.uuid4()))
    raised_on = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    ticket_id = db.Column(db.String(8), default=org_id())
    status = db.Column(db.String(32), default='Pending') # pending, completed, in review
    reason = db.Column(db.Text, nullable=False)
    raised_by = db.Column(GUID(), db.ForeignKey('user.id'), nullable=False)

    def as_dict(self):
        return {col.name: str(getattr(self, col.name)) for col in self.__table__.columns}


class Token(db.Model):
    __tablename__ = 'token'
    
    id = db.Column(GUID(), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Pending') #status = pending, acccepted, rejected
    test_id = db.Column(GUID(), db.ForeignKey('test.id'), nullable=False)
    user_id = db.Column(GUID(), db.ForeignKey('user.id'), nullable=False)

    def as_dict(self):
        return {col.name: str(getattr(self, col.name)) for col in self.__table__.columns}


@event.listens_for(Test, 'after_insert')
def scheduler_event(mapper, connection, target):
    test_id = target.id
    bg_jobs.scheduler.add_job(bg_jobs.schedule_test, args=[test_id, target.conducted_on, target.ends_on])


# @event.listens_for(User, 'after_insert')
# def create_tests(mapper, connection, target):
#     user_id = target.id
#     bg_jobs.scheduler.add_job(bg_jobs.create_test, args=[user_id, target.registered_on])


@event.listens_for(Token, 'after_update')
def reschedule_test(mapper, connection, target):
    if target.status == 'approved':
        now = datetime.datetime.now()
        starts = now + datetime.timedelta(0)
        ends = now + datetime.timedelta(7)
        test_schedule = TestSchedule.__table__
        connection.execute(
            test_schedule.update().
            where(test_schedule.c.user_id==target.user_id).
            where(test_schedule.c.test_id==target.test_id).
            values(
                {
                    test_schedule.c.starts_on: starts,
                    test_schedule.c.ends_on: ends
                }
            )
        )