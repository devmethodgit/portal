from config import Config
from database.database import db
from flask import Blueprint

bp = Blueprint("bp", __name__)


@bp.route("/")
def hello_world():
    return "<p>Hello, DIT!</p>", Config.ResponseStatusCode.OK


@bp.post("/<string:username>")
def add_user(username):
    db.add_user(username)
    return "<p>User was added!</p>", Config.ResponseStatusCode.OK


@bp.get("/<string:username>")
def check_user(username):
    name = db.find_user(username)

    if not name:
        return "<p>User not found!</p>", Config.ResponseStatusCode.NOT_FOUND

    return {"username": name[0]}, Config.ResponseStatusCode.OK


@bp.delete("/<string:username>")
def delete_user(username):
    name = db.find_user(username)

    if name is None:
        return "<p>User not found!</p>", Config.ResponseStatusCode.NOT_FOUND

    db.delete_user(username)
    return "<p>User was deleted!</p>", Config.ResponseStatusCode.OK
