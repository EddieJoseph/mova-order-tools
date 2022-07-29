import math
from datetime import datetime, date

import pandas as pd

bread_number = 'MIG111013000000'
reduction = 600
reduction_factor = 1.0

def reduce_bread(orders:pd.DataFrame, groups:pd.DataFrame):
    dates = []
    new_total = []
    reduction_percentages = []
    for date in pd.date_range(start='7/30/2022', end='8/6/2022', freq='1d'):

        dates.append(date)
        reduction_percentages.append(reduction / orders[(orders['Number'] == bread_number) & (orders['MenuPlanDate'] == date)]['OrderQytCU'].sum()*reduction_factor)
        new_total.append(orders[(orders['Number'] == bread_number) & (orders['MenuPlanDate'] == date)]['OrderQytCU'].sum() - reduction)

    new_orders = pd.DataFrame(columns = orders.columns, index = orders.index)
    for index, row in orders.iterrows():
        if row['Number'] == bread_number and row['OrderQytCU'] != 0 and row['MenuPlanDate'] in dates:

            reduction_percentage = reduction_percentages[dates.index(row['MenuPlanDate'])]

            row['OrderQytCU'] = math.floor(row['OrderQytCU'] - row['OrderQytCU'] * reduction_percentage)
            # row['OrderQytCU'] = math.ceil(row['OrderQytCU'] - row['OrderQytCU'] * reduction_percentage)

            if(row['OrderQytCU'] == 0):
                row['OrderQytCU'] = 1

            # print(row)
            new_orders.loc[index] = row
        else:
            new_orders.loc[index] = row

    check_total = []

    for date in pd.date_range(start='7/30/2022', end='8/6/2022', freq='1d'):
        dates.append(date)
        # reduction_percentages.append(reduction / new_orders[(new_orders['Number'] == bread_number) & (new_orders['MenuPlanDate'] == date)]['OrderQytCU'].sum()*reduction_factor)
        check_total.append(new_orders[(orders['Number'] == bread_number) & (new_orders['MenuPlanDate'] == date)]['OrderQytCU'].sum())

    for old, new in zip(new_total,check_total):
        print("order mig:",old,'order units:',new)
        if(new>old):
            print('ordered amount exceeded')

    new_orders.to_excel('OrderRecapPerDay_reduced_bread_amount.xlsx', index=False)

    # print(dates, new_total, reduction_percentages)

