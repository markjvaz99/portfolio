import pandas as pd
import os

cwd = os.getcwd()

def load_data(path):
    return pd.read_csv(path)

def clean_data(df):
    df = df[['GrLivArea', 'BedroomAbvGr', 'FullBath', 'SalePrice']]

    df = df.dropna()

    return df

def feature_engineering(df):
    df['price_per_sqft'] = df['SalePrice'] / df['GrLivArea']
    return df

def preprocess(path):
    df = load_data(path)
    df = clean_data(df)
    df = feature_engineering(df)

    df.to_csv("data/processed/cleaned.csv", index=False)
    return df

PATH = f'{cwd}/data/raw/train.csv'
preprocess(PATH)