from pandas import DataFrame
from config import ConfigEnv, Production, Development
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import requests


# Index(['LOGIN_ID', 'LOGIN', 'LAST_NAME', 'FIRST_NAME', 'SECOND_NAME', 'SNILS',
#        'PHONE', 'EMAIL', 'SPEC_NAME', 'SPEC_CODE', 'USER_ROLE', 'USER_ROLE_ID',
#        'LPU_ID', 'LPU_NAME', 'OGRN', 'MO_ID', 'MO_NAME'],
#       dtype='object')


def get_data_from_db():
    return pd.DataFrame


def get_dataframe_from_parquet():
    table = pq.read_table("src/duplication/data.parquet")
    return table.to_pandas()


def get_dataframe_from_file():
    dataframe: DataFrame = pd.read_excel(
        Development.FILE_PATH,
        dtype={"LPU_ID": str, "MO_ID": str, "OGRN": str},
    )
    table = pa.Table.from_pandas(dataframe)
    pq.write_table(table, "./data.parquet")
    return dataframe


def add_data(
    dataframe: pd.DataFrame,
    columns,
    id_column,
    data_type,
    data=None,
    data_id_set=None,
    do_request=True,
):
    if data_id_set is None:
        data_id_set = set()
    if data is None:
        data = []
    for index, row in dataframe[columns].iterrows():
        row = row.to_dict()
        row_id = row[id_column]
        if row_id in data_id_set or row_id is None:
            continue
        data_id_set.add(row_id)
        data.append(row)
    if not do_request:
        return
    response = requests.post(
        f"{Development.Web.BASE_URL}/fill/list/{data_type}",
        json=data,
    )
    assert response.status_code == ConfigEnv.ResponseStatusCode.OK


def add_users(dataframe):
    add_data(dataframe, *ConfigEnv.Columns.USER)


def add_role(dataframe):
    add_data(dataframe, *ConfigEnv.Columns.ROLE)


def add_spec(dataframe):
    add_data(dataframe, *ConfigEnv.Columns.SPEC)


def add_lpus(dataframe):
    data_id_set = set()
    data = []
    add_data(dataframe, *ConfigEnv.Columns.LPU, data, data_id_set, False)
    add_data(dataframe, *ConfigEnv.Columns.MO, data, data_id_set)


def lpu_to_mo(dataframe):
    add_data(dataframe, *ConfigEnv.Columns.LPU_TO_MO)


def main():
    if ConfigEnv.ENV == "development":
        if Development.FILE_PATH:
            df = get_dataframe_from_file()
        else:
            df = get_dataframe_from_parquet()
    else:
        df = get_data_from_db()
    add_users(df)
    add_role(df)
    add_spec(df)
    add_lpus(df)
    lpu_to_mo(df)


if __name__ == "__main__":
    main()
