from .database import db
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import event, text


"""
CREATE TABLE role (
    id SERIAL PRIMARY KEY,
    role_id INTEGER UNIQUE,
    role_name VARCHAR(64) NOT NULL
);

CREATE TABLE lpus (
    id SERIAL PRIMARY KEY,
    lpus_id INTEGER UNIQUE,
    lpus_name VARCHAR(255) NOT NULL,
    ogrn VARCHAR(16) NOT NULL
);

CREATE TABLE specialties (
    id SERIAL PRIMARY KEY,
    spec_code INTEGER UNIQUE,
    spec_name VARCHAR(255) NOT NULL
);

CREATE TABLE users_additional_info (
    user_id INTEGER PRIMARY KEY REFERENCES users (id),
    phone VARCHAR(16),
    email VARCHAR(255)
);

CREATE TABLE users_to_role (
    users_id INTEGER PRIMARY KEY REFERENCES users (id),
    role_id INTEGER REFERENCES role (id)
);

CREATE TABLE user_to_specialisation (
    users_id INTEGER PRIMARY KEY REFERENCES users (id),
    spec_id INTEGER REFERENCES specialties (id)
);

CREATE TABLE user_to_lpu (
    users_id INTEGER PRIMARY KEY REFERENCES users (id),
    lpus_id INTEGER REFERENCES lpus (id)
);

CREATE TABLE lpus_to_mo (
    lpus_id INTEGER PRIMARY KEY REFERENCES lpus (id),
    mo_id INTEGER NOT NULL REFERENCES lpus (id)
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    login VARCHAR(128),
    last_name VARCHAR(64),
    first_name VARCHAR(64),
    second_name VARCHAR(64),
    snils VARCHAR(12),
    created_at TIMESTAMPTZ NOT NULL,
    changed_at TIMESTAMPTZ,
    FOREIGN KEY (id) REFERENCES users_additional_info (user_id)
);


CREATE OR REPLACE FUNCTION update_time()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE users
    SET changed_at = NOW() 
    WHERE id = NEW.users_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER update_time_trigger_usc
AFTER UPDATE ON user_to_specialisation
FOR EACH ROW
EXECUTE FUNCTION update_time();

CREATE TRIGGER update_time_trigger_utr
AFTER UPDATE ON users_to_role 
FOR EACH ROW
EXECUTE FUNCTION update_time();

CREATE TRIGGER update_time_trigger_utl
AFTER UPDATE ON user_to_lpu 
FOR EACH ROW
EXECUTE FUNCTION update_time();

CREATE OR REPLACE FUNCTION update_changed_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.changed_at := NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_time_trigger_u
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_changed_at();

CREATE INDEX idx_role ON role (role_id);
CREATE INDEX idx_lpus ON lpus (lpus_id);
CREATE INDEX idx_specialties ON specialties (spec_code);
CREATE INDEX idx_users_additional_info ON users_additional_info (user_id);
CREATE INDEX idx_users_to_role ON users_to_role (users_id, role_id);
CREATE INDEX idx_users_to_specialisation ON users_to_specialisation (users_id, spec_id);
CREATE INDEX idx_user_to_lpu ON user_to_lpu (users_id, lpus_id);
CREATE INDEX idx_lpus_to_mo ON lpus_to_mo (mo_id, lpus_id);
CREATE INDEX idx_users ON users (login);
"""


class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, unique=True)
    role_name = db.Column(db.String(128), nullable=False)

    def __init__(self, data: dict):
        self.role_id = data["USER_ROLE_ID"]
        self.role_name = data["USER_ROLE"]


class Lpu(db.Model):
    __tablename__ = "lpus"
    id = db.Column(db.String(32), primary_key=True)
    lpu_name = db.Column(db.String(255))
    ogrn = db.Column(db.String(16))

    def __init__(self, data: dict):
        self.id = data["LPU_ID"] if "LPU_ID" in data else data["MO_ID"]
        self.lpu_name = data["LPU_NAME"] if "LPU_NAME" in data else data["MO_NAME"]
        self.ogrn = data["OGRN"] if "OGRN" in data else None


class Specialties(db.Model):
    __tablename__ = "specialties"
    id = db.Column(db.Integer, primary_key=True)
    spec_code = db.Column(db.Integer, unique=True)
    spec_name = db.Column(db.String(255), nullable=False)

    def __init__(self, data):
        self.spec_code = data["SPEC_CODE"]
        self.spec_name = data["SPEC_NAME"]


class UsersRole(db.Model):
    __tablename__ = "users_to_role"
    users_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True,
        nullable=False,
    )
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now())
    changed_at = db.Column(db.DateTime(timezone=True))

    def __init__(self, data: dict):
        self.users_id = data["USER_ID"]
        self.role_id = data["USER_ROLE_ID"]


class UsersSpec(db.Model):
    __tablename__ = "users_to_specialisation"
    users_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True,
        nullable=False,
    )
    spec_id = db.Column(db.Integer, db.ForeignKey("specialties.id"))
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now())
    changed_at = db.Column(db.DateTime(timezone=True))

    def __init__(self, data: dict):
        self.users_id = data["USER_ID"]
        self.spec_id = data["SPEC_CODE"]


class UsersLpu(db.Model):
    __tablename__ = "users_to_lpu"
    users_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True,
        nullable=False,
    )
    lpu_id = db.Column(db.Integer, db.ForeignKey("lpu.id"))
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now())
    changed_at = db.Column(db.DateTime(timezone=True))


class LpusMo(db.Model):
    __tablename__ = "lpus_to_mo"
    lpu_id = db.Column(
        db.String(32),
        db.ForeignKey("lpus.id"),
        primary_key=True,
        nullable=False,
    )
    mo_id = db.Column(
        db.String(32),
        db.ForeignKey("lpus.id"),
    )
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now())
    changed_at = db.Column(db.DateTime(timezone=True))

    def __init__(self, data: dict):
        self.lpu_id = data["LPU_ID"]
        self.mo_id = data["MO_ID"]


class AdditionalInfo(db.Model):
    __tablename__ = "users_additional_info"
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True,
        nullable=False,
    )
    phone = db.Column(db.String(64))
    email = db.Column(db.String(255))

    def __init__(self, data: dict):
        self.user_id = data.get("USER_ID")
        self.phone = data.get("PHONE", None)
        self.email = data.get("EMAIL", None)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(
        db.Integer,
        primary_key=True,
        nullable=False,
    )
    login = db.Column(db.String(128), unique=True)
    last_name = db.Column(db.String(64))
    first_name = db.Column(db.String(64))
    second_name = db.Column(db.String(64))
    snils = db.Column(db.String(12))
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now())
    changed_at = db.Column(db.DateTime(timezone=True))

    def __init__(self, data: dict):
        self.login = data.get("LOGIN")
        self.last_name = data.get("LAST_NAME", None)
        self.first_name = data.get("FIRST_NAME", None)
        self.second_name = data.get("SECOND_NAME", None)
        self.snils = data.get("SNILS", None)

    lpu = relationship(UsersLpu, backref="user", cascade="all, delete-orphan")
    role = relationship(UsersRole, backref="user", cascade="all, delete-orphan")
    spec = relationship(UsersSpec, backref="user", cascade="all, delete-orphan")
    addit = relationship(AdditionalInfo, backref="user", cascade="all, delete-orphan")


@event.listens_for(AdditionalInfo, "before_update")
def user_update_handler(mapper, connection, target):
    connection.execute(
        text("UPDATE users SET changed_at = NOW() WHERE id = :user_id").params(
            user_id=target.users_id
        )
    )


@event.listens_for(UsersRole, "before_update")
@event.listens_for(UsersLpu, "before_update")
@event.listens_for(UsersSpec, "before_update")
def user_update_handler(mapper, connection, target: User):
    target.changed_at = datetime.now()


@event.listens_for(User, "before_update")
def user_update_handler(mapper, connection, target: User):
    target.changed_at = datetime.now()
