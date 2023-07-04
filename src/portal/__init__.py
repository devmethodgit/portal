import time
import os

from flask import Flask

from database.database import db
from config import ConfigDB
from .data_routes import data_bp
from .celery_routes import celery_bp


def create_app():
    app = Flask(__name__)

    with app.app_context():
        app.register_blueprint(data_bp, url_prefix="/data")
        app.register_blueprint(celery_bp, url_prefix="/celery")
        app.config.from_object(ConfigDB)

        db.init_app(app)
        # wait for the database to load
        if "DOCKER_CONTAINER" in os.environ:
            time.sleep(15)
        return app
