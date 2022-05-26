import pandas as pd

def read_groups():
    df = pd.read_excel('Einheiten.xlsx', sheet_name=0)
    return df

def read_orders():
    df = pd.read_excel('Bestellung.xlsx', sheet_name=0)
    return df