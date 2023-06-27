import os
from dotenv import load_dotenv

assert load_dotenv(
    ".env"
), """Can't load the environment:(
                                        Set in .env file: 
                                        if DB env:
                                            DB_USER=
                                            DB_PASSWORD=
                                            DB_NAME=
                                            DB_HOST=
                                            DB_PORT=
                                            DB_TIMEZONE= (for example: Europe/Moscow)
                                        FLASK_ENV=production/development
                                        """


class Config:
    pass


class ConfigDB(Config):
    class DataBase:
        PASSWORD = os.environ.get("DB_PASSWORD")
        HOST = os.environ.get("DB_HOST")
        DB = os.environ.get("DB_NAME")
        USERNAME = os.environ.get("DB_USER")
        PORT = os.environ.get("DB_PORT")
        SQLALCHEMY_DATABASE_URI = (
            f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}"
        )


class ConfigApp(ConfigDB):
    class Web:
        PORT = 5000
        HOST = "0.0.0.0"
        DEBUG = True

        BASE_URL = f"http://{HOST}:{PORT}"

    class ResponseStatusCode:
        OK = 200
        NOT_FOUND = 404
        BAD_REQUEST = 400


class ConfigEnv(ConfigApp):
    ENV = os.environ.get("FLASK_ENV")

    class Columns:
        USER = [
            [
                "LOGIN",
                "EMAIL",
                "SNILS",
                "PHONE",
            ],
            "LOGIN",
            "userAndInfo",
        ]

        ROLE = [
            [
                "USER_ROLE_ID",
                "USER_ROLE",
            ],
            "USER_ROLE_ID",
            "role",
        ]
        SPEC = [
            [
                "SPEC_CODE",
                "SPEC_NAME",
            ],
            "SPEC_CODE",
            "spec",
        ]
        LPU = [["LPU_ID", "LPU_NAME", "OGRN"], "LPU_ID", "lpu"]
        LPU_TO_MO = [["LPU_ID", "MO_ID"], "LPU_ID", "lpuToMo"]
        MO = [["MO_ID", "MO_NAME"], "MO_ID", "lpu"]


class Production(ConfigApp):
    pass


class Development(ConfigApp):
    FILE_PATH = os.environ.get("SECRET_PATH", None)
