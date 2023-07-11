import pandas as pd

from duplication.dataframes import get_dataframe_from_parquet


def unique_test():
    df = get_dataframe_from_parquet()
    duplicated_logins = df.duplicated(subset=["LOGIN"], keep=False)
    differences: pd.DataFrame = df[duplicated_logins].groupby("LOGIN").nunique()

    differences = differences.loc[:, ~differences.eq(1).all()]
    print("Данные повторяются в: ", differences.columns)


if __name__ == "__main__":
    unique_test()
