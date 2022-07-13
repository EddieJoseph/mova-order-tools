import pandas as pd

def read_groups(groups_path:str='Einheiten.xlsx'):
    df = pd.read_excel(groups_path, sheet_name=0)
    return df

def read_orders(orders_path:str):
    df = pd.read_excel(orders_path, sheet_name=0)
    return df

def read_prices(prices_path:str):
    df = pd.read_excel(prices_path, sheet_name=0)
    return df

def read_classification(classification_path:str):
    df = pd.read_excel(classification_path, sheet_name=0)
    return df