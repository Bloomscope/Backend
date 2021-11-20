from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_praetorian import Praetorian
import flask_cors
import flask_bcrypt


db = SQLAlchemy()
guard = Praetorian()
cors = flask_cors.CORS()
bcrypt = flask_bcrypt.Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    from .auth import routes as auth_routes

    app.register_blueprint(auth_routes.auth)

    db.init_app(app)
    guard.init_app(app)
    cors.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        db.create_all()
    return app