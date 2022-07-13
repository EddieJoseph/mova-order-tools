import pandas as pd

from get_path import get_orders_path, get_groups_path, get_price_path, get_classification_path
from order_report_generator import generate_order_reports, expand_groups
from pickinglist_generator import generate_picking_lists
from price_calculator import generate_price_report
from read_file import read_groups, read_orders, read_prices, read_classification

if __name__ == '__main__':
    orders_path = get_orders_path()
    groups_path = get_groups_path()
    price_path = get_price_path()
    classification_path = get_classification_path()


    with pd.option_context('display.max_rows', 20,'display.max_columns', None,'display.precision', 3,'display.width', None):
        # print("sadasdasd",read_prices(price_path))

        groups = read_groups(groups_path)
        orders = read_orders(orders_path)
        prices = read_prices(price_path)
        classification = read_classification(classification_path)


        #generate_price_report(orders, groups, prices)
        # generate_order_reports(orders,groups)
        generate_picking_lists(orders, groups, prices, classification)

