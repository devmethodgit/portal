from database.database import db
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

"""


class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, unique=True)
    role_name = db.Column(db.String(64), nullable=False)


class Lpu(db.Model):
    __tablename__ = "lpus"
    id = db.Column(db.Integer, primary_key=True)
    lpus_id = db.Column(db.Integer, unique=True)
    lpus_name = db.Column(db.String(255), nullable=False)
    ogrn = db.Column(db.String(16), nullable=False)


class Specialties(db.Model):
    __tablename__ = "specialties"
    id = db.Column(db.Integer, primary_key=True)
    spec_code = db.Column(db.Integer, unique=True)
    spec_name = db.Column(db.String(255), nullable=False)

    def __init__(self, data):
        self.spec_code = data["spec_code"]
        self.spec_name = data["spec_name"]


class AdditionalInfo(db.Model):
    __tablename__ = "users_additional_info"
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True,
        nullable=False,
    )
    phone = db.Column(db.String(16))
    email = db.Column(db.String(255))


class UsersRole(db.Model):
    __tablename__ = "users_to_role"
    users_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True,
        nullable=False,
    )
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))


class UsersSpec(db.Model):
    __tablename__ = "user_to_specialisation"
    users_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True,
        nullable=False,
    )
    spec_id = db.Column(db.Integer, db.ForeignKey("specialties.id"))


class UsersLpu(db.Model):
    __tablename__ = "user_to_lpu"
    users_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True,
        nullable=False,
    )
    lpus_id = db.Column(db.Integer, db.ForeignKey("lpus.id"))


class LpusMo(db.Model):
    __tablename__ = "lpus_to_mo"
    lpus_id = db.Column(
        db.Integer,
        db.ForeignKey("lpus.id"),
        primary_key=True,
        nullable=False,
    )
    mo_id = db.Column(
        db.Integer,
        db.ForeignKey("lpus.id"),
        nullable=False,
    )


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(
        db.Integer,
        primary_key=True,
        nullable=False,
    )
    login = db.Column(db.String(128))
    last_name = db.Column(db.String(64))
    first_name = db.Column(db.String(64))
    second_name = db.Column(db.String(64))
    snils = db.Column(db.String(12))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)
    changed_at = db.Column(db.DateTime(timezone=True))

    def __init__(self, data):
        self.login = data["login"]
        self.last_name = data["last_name"]
        self.first_name = data["first_name"]
        self.second_name = data["second_name"]
        self.snils = data["snils"]
        self.created_at = datetime.now()

    lpu = relationship(UsersLpu, backref="user", cascade="all, delete-orphan")
    role = relationship(UsersRole, backref="user", cascade="all, delete-orphan")
    spec = relationship(UsersSpec, backref="user", cascade="all, delete-orphan")
    addit = relationship(AdditionalInfo, backref="user", cascade="all, delete-orphan")


@event.listens_for(UsersRole, "before_update")
@event.listens_for(UsersLpu, "before_update")
@event.listens_for(UsersSpec, "before_update")
def user_update_handler(mapper, connection, target):
    connection.execute(
        text("UPDATE users SET changed_at = NOW() WHERE id = :user_id").params(
            user_id=target.users_id
        )
    )


@event.listens_for(User, "before_update")
def user_update_handler(mapper, connection, target: User):
    target.changed_at = datetime.now()
