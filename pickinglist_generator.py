import os
import shutil
import subprocess

import pandas as pd
from joblib import Parallel, delayed

from order_report_generator import tex_escape
from price_calculator import expand_kids


def generate_picking_lists(orders: pd.DataFrame, groups: pd.DataFrame, prices: pd.DataFrame, classification: pd.DataFrame):
    kitchens = expand_kids(groups)

    KID = []
    classes = []
    for index, row in orders.iterrows():
        try:
            KID.append(groups[groups['Einheitsnummer, '] == row['Einheitsnummer']]['KüchenId, '].values[0])
        except:
            print('Group not found',row['Einheitsnummer'])
            KID.append('NaN')

        try:
            classes.append(classification[classification['Movanummer'] == row['Number']]['Kategorie numerisch'].values[0])
        except:
            print('Product not found in classification', row['Number'])
            classes.append('NaN')

    #orders['CurrentPriceCU'] = current_price
    orders['KID'] = KID
    #orders['Cost'] = orders['OrderQytCU'] * orders['CurrentPriceCU']
    orders['Class'] = classes

    #print(orders)
    generate_pickinglists(kitchens, orders)

def generate_pickinglists(kitchens:pd.DataFrame, orders:pd.DataFrame):
    for k_index, k_row in kitchens.iterrows():
        # results = Parallel(n_jobs=8)(delayed(generate_pickinglist_for_kitchen)(orders[(orders['KID'] == k_row['KüchenId, ']) & (orders['MenuPlanDate'] == date)],k_row,date) for date in pd.date_range(k_row['Startdatum'], k_row['Enddatum'], freq='1d'))
        for date in pd.date_range(k_row['Startdatum'], k_row['Enddatum'], freq='1d'):
            if(k_row['KüchenId, '] == "K_40"):
            # if(k_index == 1):
                print(k_row['KüchenId, '], orders['MenuPlanDate'], orders[(orders['KID'] == k_row['KüchenId, ']) & (orders['MenuPlanDate'] == date)])
                generate_pickinglist_for_kitchen(orders[(orders['KID'] == k_row['KüchenId, ']) & (orders['MenuPlanDate'] == date)],k_row,date)

def setup_first_table(kitchen, date, f):
    i = open(
        "resources/picking_helper_files/0_setup_first_table" + ".tex",
        "r")
    a = i.read()
    a = a.replace("$KUECHENID$", tex_escape(str(kitchen['KüchenId, '])))
    a = a.replace("$DATUM$", tex_escape(str(date.strftime('%d.%m.%Y'))))
    a = a.replace("$EINHEITSIDS$", tex_escape(str(kitchen['einheitsnummern'])))
    f.write(a)

def first_table_line(order, f):
    i = open(
        "resources/picking_helper_files/1_first_table_line" + ".tex",
        "r")
    a = i.read()
    a = a.replace("$ARTIKELNR$", tex_escape(str(order['Number'])))
    a = a.replace("$ARTIKELNAME$", tex_escape(str(order['Name'])))
    a = a.replace("$CUSIZE$", tex_escape("{:.3f}".format(order['OrderSizeKGL'])))
    a = a.replace("$AMOUNT$", tex_escape("{:.0f}".format(order['OrderQytCU'])))
    f.write(a)

def setup_second_table(kitchen, f):
    i = open(
        "resources/picking_helper_files/2_setup_second_table" + ".tex",
        "r")
    a = i.read()
    #a = a.replace("$DATE$", tex_escape(str(date.strftime('&A %d.%m.%Y'))))
    f.write(a)

def setup_third_table(kitchen, f):
    i = open(
        "resources/picking_helper_files/3_setup_third_table" + ".tex",
        "r")
    a = i.read()
    #a = a.replace("$DATE$", tex_escape(str(date.strftime('&A %d.%m.%Y'))))
    f.write(a)

def third_table_line(order, f):
    i = open(
        "resources/picking_helper_files/4_third_table_line"+ ".tex",
        "r")
    a = i.read()
    a = a.replace("$ARTIKELNR$", tex_escape(str(order['Number'])))
    a = a.replace("$ARTIKELNAME$", tex_escape(str(order['Name'])))
    a = a.replace("$CUSIZE$", tex_escape("{:.3f}".format(order['OrderSizeKGL'])))
    a = a.replace("$AMOUNT$", tex_escape("{:.0f}".format(order['OrderQytCU'])))
    f.write(a)

def end_document(kitchen,f):
    i = open(
        "resources/picking_helper_files/5_end_document" + ".tex",
        "r")
    a = i.read()
    f.write(a)


def generate_pickinglist_for_kitchen(orders:pd.DataFrame, kitchen:pd.Series, date):
    filename = "target/pickinglist_generation/Bestellung_" + str(kitchen['KüchenId, ']) + "_" + str(date.strftime('%d.%m.%Y')) + ".tex"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        setup_first_table(kitchen,date,f)
        for index, order in orders[orders['Class']==1].iterrows():
            first_table_line(order,f)
        setup_second_table(kitchen,f)
        for index, order in orders[orders['Class']==2].iterrows():
            first_table_line(order,f)
        setup_third_table(kitchen,f)
        for index, order in orders[orders['Class']==3].iterrows():
            third_table_line(order,f)
        end_document(kitchen,f)

    command = "lualatex.exe -synctex=1 -interaction=nonstopmode -output-directory=target/pickinglist_generation \""+filename+"\""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    logfilename = "target/pickinglist_generation/lualatex_" + str(kitchen['KüchenId, ']) + "_" + str(date.strftime('%d.%m.%Y')) + ".log"
    os.makedirs(os.path.dirname(logfilename), exist_ok=True)
    with open(logfilename, 'w') as latex_log:
        for line in process.stdout:
            latex_log.write(str(line))
        process.wait()
        latex_log.write("Exit Code: " + str(process.returncode))
    outputfilename = "output/komissionierung/Bestellung_" + str(kitchen['KüchenId, ']) + "_" + str(date.strftime('%d.%m.%Y')) + ".pdf"
    os.makedirs(os.path.dirname(outputfilename), exist_ok=True)

    shutil.move(filename[0:-3] + "pdf", outputfilename)


