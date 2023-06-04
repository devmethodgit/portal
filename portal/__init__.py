from flask import Flask
from database import db


def create_app(**kwargs):
    """Construct the core application."""
    app = Flask(__name__, template_folder='templates')

    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        from . import routes
        return app