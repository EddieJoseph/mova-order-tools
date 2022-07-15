from datetime import datetime

import pandas as pd

def read_groups(groups_path:str='Einheiten.xlsx'):
    df = pd.read_excel(groups_path, sheet_name=0)
    return df

def read_orders(orders_path:str):
    df = pd.read_excel(orders_path, sheet_name=0)

    if df[(df['MenuPlanDate'] < datetime.strptime('23.7.22', '%d.%m.%y'))  | (df['MenuPlanDate'] > datetime.strptime('6.8.22', '%d.%m.%y'))].shape[0] > 0:
        raise Exception("Orders Date out of range")
    if df[(df['MenuPlanDate']=='')].shape[0] > 0:
        raise Exception("Orders Date not set")
    return df

def read_prices(prices_path:str):
    df = pd.read_excel(prices_path, sheet_name=0)
    return df

def read_classification(classification_path:str):
    df = pd.read_excel(classification_path, sheet_name=0)
    if df[(df['Kategorie numerisch']!=1)&(df['Kategorie numerisch']!=2)&(df['Kategorie numerisch']!=3)].shape[0] > 0:
        raise Exception("Classification Kategorie not set")
    if df[(df['Sortierung']=='')].shape[0] > 0:
        raise Exception("Classification Sortierung not set")
    return df