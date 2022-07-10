import pandas as pd

from get_path import get_orders_path, get_groups_path, get_price_path
from order_report_generator import generate_order_reports, expand_groups
from read_file import read_groups, read_orders, read_prices

if __name__ == '__main__':
    orders_path = get_orders_path()
    groups_path = get_groups_path()
    price_path = get_price_path()


    with pd.option_context('display.max_rows', 20,'display.max_columns', None,'display.precision', 3,'display.width', None):
        # print(expand_groups(read_groups(groups_path)))

        groups = read_groups(groups_path)
        orders = read_orders(orders_path)
        prices = read_prices(price_path)

        generate_order_reports(orders,groups,prices)