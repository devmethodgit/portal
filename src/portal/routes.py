from config import Config
from database.models import *
from flask import Blueprint, request, jsonify
from database.database import db

user_bp = Blueprint("user", __name__)


@user_bp.route("/test")
def test_page():
    return jsonify(message="Hello, DIT!"), Config.ResponseStatusCode.OK


@user_bp.post("/")
def add_user():
    data = request.get_json()
    user = User(data)
    user.user_login = UserLogins(data)
    db.session.add(user)
    db.session.commit()
    return (
        jsonify(message="User added!", login_id=user.login_id),
        Config.ResponseStatusCode.OK,
    )


@user_bp.delete("/<int:login_id>")
def delete_user(login_id):
    user_login = UserLogins.query.filter_by(login_id=login_id).first()

    if user_login is None:
        return jsonify(message="User not founded!"), Config.ResponseStatusCode.NOT_FOUND

    db.session.delete(user_login)
    db.session.commit()

    return jsonify(message="User deleted!"), Config.ResponseStatusCode.OK


@user_bp.get("/<int:login_id>")
def check_user(login_id):
    user = User.query.filter_by(login_id=login_id).first()

    if user is None:
        return jsonify(message="User not founded!"), Config.ResponseStatusCode.NOT_FOUND

    user_dict = {
        "last_name": user.last_name,
        "first_name": user.first_name,
        "second_name": user.second_name,
        "snils": user.snils,
        "login": user.user_login.login,
    }

    return (
        jsonify(message="User founded!", data=user_dict),
        Config.ResponseStatusCode.OK,
    )
