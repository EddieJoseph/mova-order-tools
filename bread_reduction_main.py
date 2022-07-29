import pandas as pd

from bread_reduction import reduce_bread
from get_path import get_orders_path, get_groups_path
from read_file import read_orders, read_groups

if __name__ == '__main__':
    orders_path = get_orders_path()
    groups_path = get_groups_path()

    with pd.option_context('display.max_rows', 20, 'display.max_columns', None, 'display.precision', 3, 'display.width',
                           None):
        groups = read_groups(groups_path)
        orders = read_orders(orders_path)

        reduce_bread(orders, groups)
