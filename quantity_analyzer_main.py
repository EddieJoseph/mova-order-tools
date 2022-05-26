from analyzer import run_analysis
from get_path import get_orders_path
from read_file import read_groups, read_orders

if __name__ == '__main__':
    orders_path = get_orders_path()
    groups = read_groups()
    orders = read_orders(orders_path)
    # print(groups)
    # print(orders)
    run_analysis(groups,orders)
