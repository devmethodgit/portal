import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from config import ConfigEnv
from celdery.red import redis_client
from duplication.first_duplic import (
    get_dataframe_from_parquet,
    get_df,
    add_users,
    get_user_df,
    delete_users,
    save_to_parquet,
    main,
)


def get_merged_dfs():
    old_df = get_dataframe_from_parquet()
    new_df = get_df()
    result = old_df.merge(new_df, how="outer", indicator=True)
    without_both = result[result["_merge"] != "both"]
    for_del_df = without_both[without_both["_merge"] == "left_only"]
    for_add_df = without_both[without_both["_merge"] != "left_only"]
    result.drop("_merge", axis=1, inplace=True)
    return {
        "add": for_add_df,
        "del": for_del_df,
        "all_data": result,
    }


def update_users(dataframes: dict[str, pd.DataFrame]):
    add_users_df = get_user_df(dataframes["add"])
    add_users(add_users_df)

    del_users_df = get_user_df(dataframes["del"])
    delete_users(del_users_df)


def update_parquet(dataframes: dict[str, pd.DataFrame]):
    # parquet does not support delete rows, but support append
    if not dataframes["del"].empty:
        save_to_parquet(dataframes["all_data"])
        return
    parquet_data = pq.ParquetDataset(ConfigEnv.PARQUET_PATH)
    schema = parquet_data.schema
    table = pa.Table.from_pandas(df=dataframes["add"], schema=schema)

    with pq.ParquetWriter(ConfigEnv.PARQUET_PATH, schema) as writer:
        writer.write_table(table)


def main_update():
    if not redis_client.get("data_in_parquet"):
        main()
        return
    dataframes = get_merged_dfs()
    update_users(dataframes)
    update_parquet(dataframes)
