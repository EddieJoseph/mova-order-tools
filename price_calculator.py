import pandas as pd


def generate_price_report(orders: pd.DataFrame, groups: pd.DataFrame, prices: pd.DataFrame):
    current_price = []
    for index, row in orders.iterrows():
        try:
            current_price.append(prices[prices['Number'] == row['Number']]['OrderPriceInCU'].values[0])
        except:
            print('Price missing', row['Number'], index)
            current_price.append(0)
    orders['CurrentPriceCU'] = current_price
    orders['Cost'] = orders['OrderQytCU'] * orders['CurrentPriceCU']

    # print(current_price)
    group_cost_per_day = calculate_daily_prices(orders, groups)
    group_cost_per_day.to_excel('Tageskosten.xlsx')


# MIG111013000000


def calculate_daily_prices(orders: pd.DataFrame, groups: pd.DataFrame):
    for date in pd.date_range('2022-07-22', '2022-08-08', freq='1d'):
        orders_day = orders[orders['MenuPlanDate'] == date]
        cost_day = [];
        for index, row in groups.iterrows():
            cost_day.append(orders_day[orders_day['Einheitsnummer'] == row['Einheitsnummer, ']]['Cost'].sum())
        groups[date] = cost_day
    return groups
