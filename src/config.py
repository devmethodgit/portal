import os
from dotenv import load_dotenv

assert load_dotenv(
    ".env"
), """Can't load the environment:(
                                DB_USER=
                                DB_PASSWORD=
                                DB_NAME=
                                DB_HOST=
                                DB_PORT=
                            """


class Config:
    class DataBase:
        PASSWORD = os.environ.get("DB_PASSWORD")
        HOST = os.environ.get("DB_HOST")
        DB = os.environ.get("DB_NAME")
        USERNAME = os.environ.get("DB_USER")
        PORT = os.environ.get("DB_PORT")

    class Web:
        PORT = 5000
        HOST = "0.0.0.0"
        DEBUG = True

    class ResponseStatusCode:
        OK = 200
        NOT_FOUND = 404
        BAD_REQUEST = 400

    BASE_URL = f"http://{Web.HOST}:{Web.PORT}"


class Appication:
    SQLALCHEMY_DATABASE_URI = f"postgresql://{Config.DataBase.USERNAME}:{Config.DataBase.PASSWORD}@{Config.DataBase.HOST}:{Config.DataBase.PORT}/{Config.DataBase.DB}"
