from config import ConfigApp
from flask import Blueprint, request, jsonify
from database.database import db
from database.models import (
    User,
    UsersSpec,
    Specialties,
    AdditionalInfo,
    Role,
    Lpu,
    LpusMo,
)

data_bp = Blueprint("data", __name__)
fill_tables_bp = Blueprint("fill", __name__)
Config = ConfigApp()


@data_bp.get("/test")
def test_page():
    return jsonify(message="Hello, DIT!"), Config.ResponseStatusCode.OK


@data_bp.post("/")
def add_user():
    data = request.get_json()
    user = User(data)
    db.session.add(user)
    db.session.commit()
    return (
        jsonify(message="User added!", user_id=user.id),
        Config.ResponseStatusCode.OK,
    )


@data_bp.get("/filial/<int:lpu_id>")
def get_filial(lpu_id):
    filials = [lpu.lpu_id for lpu in LpusMo.query.filter(LpusMo.mo_id == lpu_id)]
    return (
        jsonify(message=f"Filials of {lpu_id}!", filleals=filials),
        Config.ResponseStatusCode.OK,
    )


@data_bp.delete("/<int:user_id>")
def delete_user(user_id):
    user = User.query.filter(User.id == user_id).first()

    if user is None:
        return jsonify(message="User not founded!"), Config.ResponseStatusCode.NOT_FOUND

    db.session.delete(user)
    db.session.commit()

    return jsonify(message="User deleted!"), Config.ResponseStatusCode.OK


@data_bp.get("/<int:user_id>")
def check_user(user_id):
    user = User.query.filter(User.id == user_id).first()

    if user is None:
        return jsonify(message="User not founded!"), Config.ResponseStatusCode.NOT_FOUND

    user_dict = {
        "LAST_NAME": user.last_name,
        "FIRST_NAME": user.first_name,
        "SECOND_NAME": user.second_name,
        "SNILS": user.snils,
        "LOGIN": user.login,
    }

    return (
        jsonify(message="User founded!", user=user_dict),
        Config.ResponseStatusCode.OK,
    )


@data_bp.post("/spec/<int:user_id>/<int:spec_id>")
def add_user_to_spec(user_id, spec_id):
    db.session.add(UsersSpec(users_id=user_id, spec_id=spec_id))
    db.session.commit()
    return (
        jsonify(message="User to spec added!"),
        Config.ResponseStatusCode.OK,
    )


@data_bp.post("/addInfo")
def add_additional_info():
    data = request.get_json()
    db.session.add(AdditionalInfo(data))
    db.session.commit()
    return (
        jsonify(message="Info was added!"),
        Config.ResponseStatusCode.OK,
    )


@data_bp.get("/spec/<int:user_id>")
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


@fill_tables_bp.post("/list/userAndInfo")
def add_list_user_and_info():
    data = request.get_json()
    users = [User(user_data) for user_data in data]
    db.session.add_all(users)
    db.session.commit()
    for i in range(len(users)):
        data[i]["USER_ID"] = users[i].id
    add_infos = [AdditionalInfo(info) for info in data]
    db.session.add_all(add_infos)
    db.session.commit()
    return (
        jsonify(message="Info was added!"),
        Config.ResponseStatusCode.OK,
    )


@fill_tables_bp.post("/list/addInfo")
def add_list_addit_info():
    add_infos = [AdditionalInfo(info) for info in request.get_json()]
    db.session.add_all(add_infos)
    db.session.commit()
    return (
        jsonify(message="Info was added!"),
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
        "SPEC_CODE": spec.spec_code,
        "SPEC_NAME": spec.spec_name,
    }

    return (
        jsonify(message="Spec founded!", spec=spec_dict),
        Config.ResponseStatusCode.OK,
    )


@fill_tables_bp.post("/list/user")
def add_list_user():
    users = [User(user_data) for user_data in request.get_json()]
    db.session.add_all(users)
    db.session.commit()
    users_id = [user.id for user in users]
    return (
        jsonify(message="User added!", users_id=users_id),
        Config.ResponseStatusCode.OK,
    )


@fill_tables_bp.post("/list/role")
def add_list_role():
    roles = [Role(role_data) for role_data in request.get_json()]
    db.session.add_all(roles)
    db.session.commit()
    return (
        jsonify(message="Role added!"),
        Config.ResponseStatusCode.OK,
    )


@fill_tables_bp.post("/list/spec")
def add_list_spec():
    specs = [Specialties(spec_data) for spec_data in request.get_json()]
    db.session.add_all(specs)
    db.session.commit()
    return (
        jsonify(message="Spec added!"),
        Config.ResponseStatusCode.OK,
    )


@fill_tables_bp.post("/list/lpu")
def add_list_lpus():
    lpus = [Lpu(lpu_data) for lpu_data in request.get_json()]
    db.session.add_all(lpus)
    db.session.commit()
    return (
        jsonify(message="Lpus added!"),
        Config.ResponseStatusCode.OK,
    )


@fill_tables_bp.post("/list/lpuToMo")
def add_list_lpu_to_mo():
    lpus_to_mo = [LpusMo(lpu_to_mo) for lpu_to_mo in request.get_json()]
    db.session.add_all(lpus_to_mo)
    db.session.commit()
    return (
        jsonify(message="Lpus to mo added!"),
        Config.ResponseStatusCode.OK,
    )
