from config import Config
from database.models import User
from database.database import db
from flask import Blueprint

bp = Blueprint("bp", __name__)


@bp.route("/")
def hello_world():
    return "<p>Hello, DIT!</p>", Config.ResponseStatusCode.OK


@bp.post("/<string:username>")
def add_user(username):
    user = User(username=username)
    db.session.add(user)
    db.session.commit()
    return "<p>User was added!</p>", Config.ResponseStatusCode.OK


@bp.delete("/<string:username>")
def delete_user(username):
    user = User.query.filter_by(username=username).first()

    if user is None:
        return "<p>User not found!</p>", Config.ResponseStatusCode.NOT_FOUND

    db.session.delete(user)
    db.session.commit()

    return "<p>User was deleted!</p>", Config.ResponseStatusCode.OK


@bp.get("/<string:username>")
def check_user(username):
    user = User.query.filter_by(username=username).first()

    if user is None:
        return "<p>User not found!</p>", Config.ResponseStatusCode.NOT_FOUND

    return {"username": user.username}, Config.ResponseStatusCode.OK
