from config import Config
from database.models import *
from flask import Blueprint, request, jsonify
from database.database import db

user_bp = Blueprint("user", __name__)
fill_tables_bp = Blueprint("fill", __name__)


@user_bp.get("/test")
def test_page():
    return jsonify(message="Hello, DIT!"), Config.ResponseStatusCode.OK


@user_bp.post("/")
def add_user():
    data = request.get_json()
    user = User(data)
    db.session.add(user)
    db.session.commit()
    return (
        jsonify(message="User added!", user_id=user.id),
        Config.ResponseStatusCode.OK,
    )


@user_bp.delete("/<int:user_id>")
def delete_user(user_id):
    user = User.query.filter(User.id == user_id).first()

    if user is None:
        return jsonify(message="User not founded!"), Config.ResponseStatusCode.NOT_FOUND

    db.session.delete(user)
    db.session.commit()

    return jsonify(message="User deleted!"), Config.ResponseStatusCode.OK


@user_bp.get("/<int:user_id>")
def check_user(user_id):
    user = User.query.filter(User.id == user_id).first()

    if user is None:
        return jsonify(message="User not founded!"), Config.ResponseStatusCode.NOT_FOUND

    user_dict = {
        "last_name": user.last_name,
        "first_name": user.first_name,
        "second_name": user.second_name,
        "snils": user.snils,
        "login": user.login,
    }

    return (
        jsonify(message="User founded!", user=user_dict),
        Config.ResponseStatusCode.OK,
    )


@user_bp.post("/spec/<int:user_id>/<int:spec_id>")
def add_user_to_spec(user_id, spec_id):
    db.session.add(UsersSpec(users_id=user_id, spec_id=spec_id))
    db.session.commit()
    return (
        jsonify(message="User to spec added!"),
        Config.ResponseStatusCode.OK,
    )


@user_bp.get("/spec/<int:user_id>")
def get_spec_id(user_id):
    user_spec = UsersSpec.query.filter(UsersSpec.users_id == user_id).first()

    if user_spec is None:
        return (
            jsonify(message="User spec not founded!"),
            Config.ResponseStatusCode.NOT_FOUND,
        )

    return (
        jsonify(message="User spec founded!", spec_id=user_spec.spec_id),
        Config.ResponseStatusCode.OK,
    )


@fill_tables_bp.post("/spec")
def add_spec():
    spec = Specialties(request.get_json())
    db.session.add(spec)
    db.session.commit()
    return (
        jsonify(message="Spec added!", spec_id=spec.id),
        Config.ResponseStatusCode.OK,
    )


@fill_tables_bp.delete("/spec/<int:spec_id>")
def delete_spec(spec_id):
    spec = Specialties.query.filter(Specialties.id == spec_id).first()

    if spec is None:
        return (
            jsonify(message="Spec not founded!"),
            Config.ResponseStatusCode.NOT_FOUND,
        )

    db.session.delete(spec)
    db.session.commit()
    return (
        jsonify(message="Spec deleted!"),
        Config.ResponseStatusCode.OK,
    )


@fill_tables_bp.get("/spec/<int:spec_id>")
def get_spec(spec_id):
    spec = Specialties.query.filter(Specialties.id == spec_id).first()
    if spec is None:
        return (
            jsonify(message="Spec not founded!"),
            Config.ResponseStatusCode.NOT_FOUND,
        )
    spec_dict = {
        "spec_code": spec.spec_code,
        "spec_name": spec.spec_name,
    }

    return (
        jsonify(message="Spec founded!", spec=spec_dict),
        Config.ResponseStatusCode.OK,
    )
