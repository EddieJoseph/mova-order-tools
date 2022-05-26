# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from analyzer import run_analysis
from get_path import get_orders_path
from read_file import read_groups, read_orders
import sys


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    orders_path = get_orders_path()

    groups = read_groups()
    orders = read_orders(orders_path)
    # print(groups)
    # print(orders)
    run_analysis(groups,orders)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
