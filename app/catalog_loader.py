import pandas as pd


def load_catalog(path="data/shl_catalog.csv"):
    df = pd.read_csv(path)
    df.fillna("", inplace=True)
    return df