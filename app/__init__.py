from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import flask_cors
import flask_bcrypt
from celery import Celery
from flask_mail import Mail
from .config import CELERY_BROKER_URL


db = SQLAlchemy()
jwt = JWTManager()
cors = flask_cors.CORS()
bcrypt = flask_bcrypt.Bcrypt()
mail = Mail()
celery = Celery(__name__, broker=CELERY_BROKER_URL)


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    from .auth import routes as auth_routes
    from .admin_dashboard import routes as admin_dash_routes
    from .errors import routes as error_handlers
    from .students import routes as student_routes
    from .parents import routes as parent_routes
    from .utils import bg_jobs as jobs
    from .payments import routes as payment_routes
    from .tokens import routes as token_routes
    from . import admin

    app.register_blueprint(auth_routes.auth)
    app.register_blueprint(admin_dash_routes.admin_dash)
    app.register_blueprint(error_handlers.errors)
    app.register_blueprint(student_routes.student)
    app.register_blueprint(parent_routes.parent)
    app.register_blueprint(jobs.job)
    app.register_blueprint(payment_routes.payment)
    app.register_blueprint(token_routes.token)

    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    admin.init_app(app, db)
    celery.conf.update(app.config)

    with app.app_context():
        db.create_all()
    return app

