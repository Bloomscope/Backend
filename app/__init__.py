from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    from .auth import routes as auth_routes

    app.register_blueprint(auth_routes.auth)

    db.init_app(app)

    with app.app_context():
        db.create_all()
    return app