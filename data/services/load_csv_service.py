import pandas as pd


def load_csv(file_path, columns, renames):
    return (pd.read_csv(file_path, encoding='latin1', usecols=columns)
            .astype(object).where(pd.notna, None)
            .rename(columns=renames))
