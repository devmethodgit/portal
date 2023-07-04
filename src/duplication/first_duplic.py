import pandas as pd
from pandas import DataFrame

from wsgi import app
from config import ConfigEnv, Development
from database.models import User
from database.database import db
from celdery.red import redis_client

# Index(['LOGIN_ID', 'LOGIN', 'LAST_NAME', 'FIRST_NAME', 'SECOND_NAME', 'SNILS',
#        'PHONE', 'EMAIL', 'SPEC_NAME', 'SPEC_CODE', 'USER_ROLE', 'USER_ROLE_ID',
#        'LPU_ID', 'LPU_NAME', 'OGRN', 'MO_ID', 'MO_NAME'],
#       dtype='object')


def get_data_from_db():
    return pd.DataFrame


def get_dataframe_from_parquet():
    return pd.read_parquet(ConfigEnv.PARQUET_PATH)


def save_to_parquet(dataframe):
    dataframe.to_parquet(ConfigEnv.PARQUET_PATH, compression="gzip")


def get_dataframe_from_file():
    dataframe: DataFrame = pd.read_excel(
        Development.EXCEL_FILE_PATH,
        dtype=str,
    )
    return dataframe


def get_df():
    if ConfigEnv.ENV == "development":
        df = get_dataframe_from_file()
    else:
        df = get_data_from_db()
    df.drop_duplicates(subset="LOGIN", inplace=True)
    return df.fillna("None")


def get_user_df(df):
    user_frame = df.loc[:, ConfigEnv.Columns.USER]
    # user_frame.drop_duplicates(subset=["LOGIN"], inplace=True)
    return user_frame


def delete_users(user_frame):
    with app.app_context():
        user_frame.apply(
            lambda x: User.query.filter(User.login == x["LOGIN"]).delete(),
            axis=1,
        )
        db.session.commit()


def add_users(user_frame):
    users = []
    user_frame.apply(lambda x: users.append(User(x)), axis=1)

    with app.app_context():
        db.session.add_all(users)
        db.session.commit()


def main():
    df = get_df()
    save_to_parquet(df)
    redis_client.set("data_in_parquet", "true")
    user_frame = get_user_df(df)
    add_users(user_frame)
