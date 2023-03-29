from flask import Flask
from .database import db
from .config import Config


def create_app():
    """
    Creates a Flask application instance and returns it along with a Celery instance.

    Returns:
        app (Flask): A Flask application instance.
        celery (Celery): A Celery instance.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app=app)

    with app.app_context():
        db.create_all()

    return app
