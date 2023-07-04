import os
from dotenv import load_dotenv
import logging


def setup_logger(filename):
    logging.basicConfig(
        level=logging.ERROR,
        filename=filename,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


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
    TZ = os.environ.get("DB_TIMEZONE")


class ConfigDB(Config):
    PASSWORD = os.environ.get("DB_PASSWORD")
    HOST = os.environ.get("DB_HOST")
    DB = os.environ.get("DB_NAME")
    USERNAME = os.environ.get("DB_USER")
    PORT = os.environ.get("DB_PORT")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}"


class ConfigApp(Config):
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
    PARQUET_PATH = "./duplication/data.parquet"

    class Columns:
        USER = ["LOGIN", "EMAIL", "SNILS", "PHONE"]

        ROLE = [
            "USER_ROLE_ID",
            "USER_ROLE",
        ]
        SPEC = [
            "SPEC_CODE",
            "SPEC_NAME",
        ]
        LPU = ["LPU_ID", "LPU_NAME", "OGRN"]
        LPU_TO_MO = ["LPU_ID", "MO_ID"]
        MO = ["MO_ID", "MO_NAME"]


class Production(Config):
    pass


class Development(Config):
    EXCEL_FILE_PATH = "./duplication/database.xlsx"
