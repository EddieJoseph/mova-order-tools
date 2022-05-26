# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from analyzer import run_analysis
from read_file import read_groups, read_orders


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    groups = read_groups()

    orders = read_orders()

    # print(groups)
    #
    # print(orders)
    run_analysis(groups,orders)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
