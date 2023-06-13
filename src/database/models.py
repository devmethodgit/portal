from database.database import db


class UserLogins(db.Model):
    __tablename__ = "users_login"
    login_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(64), nullable=False, unique=True)

    user = db.relationship(
        "User", backref="user_login", uselist=False, cascade="all,delete"
    )

    def __init__(self, data):
        self.login = data["login"]


class UserRoles(db.Model):
    __tablename__ = "users_roles"
    id = db.Column(db.Integer, primary_key=True)
    user_role_id = db.Column(db.String(16), unique=True)
    user_role = db.Column(db.String(64), nullable=False)


class Mos(db.Model):
    __tablename__ = "mos"
    id = db.Column(db.Integer, primary_key=True)
    mo_id = db.Column(db.String(16), unique=True)
    mo_name = db.Column(db.String(255), nullable=False)


class Lpus(db.Model):
    __tablename__ = "lpus"
    id = db.Column(db.Integer, primary_key=True)
    lpu_id = db.Column(db.String(16), unique=True)
    lpu_name = db.Column(db.String(255), nullable=False)
    ogrn = db.Column(db.String(16), nullable=False)
    mo_id = db.Column(db.String(16), db.ForeignKey("mos.mo_id"), nullable=False)


class Specialties(db.Model):
    __tablename__ = "specialties"
    id = db.Column(db.Integer, primary_key=True)
    spec_code = db.Column(db.String(16), unique=True)
    spec_name = db.Column(db.String(255), nullable=False)


class AdditionalInfo(db.Model):
    __tablename__ = "additional_info"
    additional_id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(12))
    email = db.Column(db.String(64))


class UsersAdditionalInfo(db.Model):
    __tablename__ = "users_additional_info"
    login_id = db.Column(
        db.Integer,
        db.ForeignKey("users_login.login_id"),
        primary_key=True,
        nullable=False,
    )
    additional_id = db.Column(
        db.Integer, db.ForeignKey("additional_info.additional_id")
    )


class UsersRole(db.Model):
    __tablename__ = "users_role"
    login_id = db.Column(
        db.Integer,
        db.ForeignKey("users_login.login_id"),
        primary_key=True,
        nullable=False,
    )
    user_role_id = db.Column(db.String(16), db.ForeignKey("users_roles.user_role_id"))


class UsersSpec(db.Model):
    __tablename__ = "users_specialisation"
    login_id = db.Column(
        db.Integer,
        db.ForeignKey("users_login.login_id"),
        primary_key=True,
        nullable=False,
    )
    spec_code = db.Column(db.String(16), db.ForeignKey("specialties.spec_code"))


class UsersLpu(db.Model):
    __tablename__ = "users_lpu"
    login_id = db.Column(
        db.Integer,
        db.ForeignKey("users_login.login_id"),
        primary_key=True,
        nullable=False,
    )
    lpu_id = db.Column(db.String(16), db.ForeignKey("lpus.lpu_id"))


class User(db.Model):
    __tablename__ = "users"
    login_id = db.Column(
        db.Integer,
        db.ForeignKey("users_login.login_id"),
        primary_key=True,
        nullable=False,
    )
    last_name = db.Column(db.String(64))
    first_name = db.Column(db.String(64))
    second_name = db.Column(db.String(64))
    snils = db.Column(db.String(12))

    def __init__(self, data):
        self.last_name = data["last_name"]
        self.first_name = data["first_name"]
        self.second_name = data["second_name"]
        self.snils = data["snils"]
