import locale
import os
import shutil

import pandas as pd
import subprocess
import re
from joblib import Parallel, delayed

def generate_order_reports(orders,groups,prices):
    print("starting order report generation.")
    expanded_groups = expand_groups(groups)

    current_price = []
    for index, row in orders.iterrows():
        try:
            current_price.append(prices[prices['Number'] == row['Number']]['OrderPriceInCU'].values[0])
        except:
            print('Price missing', row['Number'], index)
            current_price.append(0)
    orders['CurrentPriceCU'] = current_price
    orders['Cost'] = orders['OrderQytCU'] * orders['CurrentPriceCU']

    results = Parallel(n_jobs=8)(delayed(report_for_group)(orders, row) for index, row in expanded_groups.iterrows())
    # for index, row in expanded_groups.iterrows():
    #     if(index > 200 and index < 220):
    #         print(str(index) + " of " + str(len(expanded_groups)))
    #         report_for_group(orders, row)


def expand_groups(groups:pd.DataFrame):
    startdate = []
    enddate = []
    days = []
    for index, row in groups.iterrows():
        start = pd.to_datetime(row['Datum Lager'].split("-")[0],format='%d.%m.%Y')
        end = pd.to_datetime(row['Datum Lager'].split("-")[1],format='%d.%m.%Y')
        startdate.append(start)
        enddate.append(end)
        days.append((end-start).days)

    groups['Startdatum']=startdate
    groups['Enddatum'] = enddate
    groups['Tage'] = days
    groups['Budget'] = (groups['Gesamtzahl Einheit, ']+groups['Gesamtzahl Internationale Einheit, ']) * (groups['Tage']) * 8 + groups['Anzahl Besuchende'] * 2.5
    return groups



def report_for_group(orders:pd.DataFrame,group_exp:pd.Series):
    filename = "target/report_generation/Bestellung_"+str(group_exp['Einheitsnummer, '])+".tex"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename,'w') as f:
        if group_exp[' Korrespondenzsprache, '] == "it":
            locale.setlocale(locale.LC_ALL, 'it_CH')
        elif group_exp[' Korrespondenzsprache, '] == "fr":
            locale.setlocale(locale.LC_ALL, 'fr_CH')
        else:
            locale.setlocale(locale.LC_ALL, 'de_CH')

        init_file(orders.loc[orders['Einheitsnummer'] == group_exp['Einheitsnummer, ']],group_exp,f)
        for date in pd.date_range(group_exp['Startdatum'], group_exp['Enddatum'], freq='1d'):
            #print(orders)
            orders_per_group_day = orders.loc[(orders['Einheitsnummer'] == group_exp['Einheitsnummer, ']) & (orders['MenuPlanDate'] == date),['Name', 'Number', 'OrderSizeKGL', 'CurrentPriceCU', 'OrderQytCU', 'TotalOrderAmount','Cost']]
            if(orders_per_group_day.empty):
                empty_page(date, group_exp, f)
            else:
                init_page(date,group_exp,f)
                for index, row in orders_per_group_day.iterrows():
                    add_line(row,group_exp,f)
                end_page(group_exp,f)
        end_file(group_exp,f)

    command = "lualatex.exe -synctex=1 -interaction=nonstopmode -output-directory=target/report_generation \"target/report_generation/Bestellung_\""+str(group_exp['Einheitsnummer, '])+".tex"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    logfilename = "target/report_generation/lualatex_" + str(group_exp['Einheitsnummer, ']) + ".log"
    os.makedirs(os.path.dirname(logfilename), exist_ok=True)
    with open(logfilename, 'w') as latex_log:
        for line in process.stdout:
            latex_log.write(str(line))
        process.wait()
        latex_log.write("Exit Code: "+str(process.returncode))
    outputfilename = "output/bestellung/Bestellung_"+str(group_exp['Einheitsnummer, '])+".pdf"
    os.makedirs(os.path.dirname(outputfilename), exist_ok=True)

    shutil.move(filename[0:-3]+"pdf",outputfilename)

def init_file(orders:pd.DataFrame,group_exp:pd.Series,f):
    i = open("resources/report_helper_files/first_page_"+str(group_exp[' Korrespondenzsprache, '])+".tex", "r")
    a = i.read()
    cost = sum(orders['Cost'])

    a = a.replace("$NAME$", tex_escape(str(group_exp['Einheitsname,'])))
    a = a.replace("$ID$", tex_escape(str(group_exp['Einheitsnummer, '])))
    a = a.replace("$KITCHEN_ID$", tex_escape(str(group_exp['KüchenId, '])))
    a = a.replace("$CAMP_DATES$", tex_escape(str( group_exp['Datum Lager'].split('-')[0] + " - " +group_exp['Datum Lager'].split('-')[1])))
    a = a.replace("$NR_PERS$", tex_escape(str(group_exp['Gesamtzahl Einheit, '])))
    a = a.replace("$NR_INT$", tex_escape(str(group_exp['Gesamtzahl Internationale Einheit, '])))
    a = a.replace("$NR_TOTAL$", tex_escape(str(group_exp['Gesamtzahl Einheit, '] + group_exp['Gesamtzahl Internationale Einheit, '])))

    if(group_exp['Datum Besuchstag,']!='keinen Besuchstag'):
        a = a.replace("$VISIT_DATE$", tex_escape(str(group_exp['Datum Besuchstag,'])))
        a = a.replace("$VISIT_NR$", tex_escape(str(group_exp['Anzahl Besuchende'])))
    else:
        a = a.replace("$VISIT_DATE$", tex_escape(str('-')))
        a = a.replace("$VISIT_NR$", tex_escape(str('-')))
    a = a.replace("$BUSGET$", tex_escape(str(round(group_exp['Budget'],2))))
    a = a.replace("$COST$", tex_escape(str(round(cost,2))))
    a = a.replace("$REST$", tex_escape(str(round(group_exp['Budget']-cost,2))))
    f.write(a)

def end_file(group_exp:pd.Series,f):
    i = open("resources/report_helper_files/last_page_"+str(group_exp[' Korrespondenzsprache, '])+".tex", "r")
    a = i.read()
    f.write(a)

def init_page(date,group_exp:pd.Series,f):
    i = open("resources/report_helper_files/report_page_setup_"+str(group_exp[' Korrespondenzsprache, '])+".tex", "r")
    a = i.read()
    a = a.replace("$DATE$", tex_escape(str(date.strftime('%A %d.%m.%Y'))))



    f.write(a)

def empty_page(date, group_exp:pd.Series, f):
    i = open("resources/report_helper_files/report_empty_page_setup_"+str(group_exp[' Korrespondenzsprache, '])+".tex", "r")
    a = i.read()
    a = a.replace("$DATE$", tex_escape(str(date.strftime('&A %d.%m.%Y'))))
    f.write(a)

def add_line(row,group_exp:pd.Series,f):
    i = open("resources/report_helper_files/report_line_"+str(group_exp[' Korrespondenzsprache, '])+".tex", "r")
    a = i.read()
    a=a.replace("$Name$", tex_escape(str(row['Name'])))
    a=a.replace("$Number$", tex_escape(str(row['Number'])))
    a=a.replace("$OrderSizeKGL$", tex_escape("{:.3f}".format(row['OrderSizeKGL'])))
    a=a.replace("$OrderPriceInCU$", tex_escape("{:.2f}".format(round(row['CurrentPriceCU'],2))))
    a=a.replace("$OrderQtyInCU$", tex_escape("{:.2f}".format(row['OrderQytCU'])))
    a=a.replace("$Cost$", tex_escape("{:.2f}".format(round(row['Cost'],2))))
    f.write(a)

def end_page(group_exp:pd.Series,f):
    i = open("resources/report_helper_files/page_end_"+str(group_exp[' Korrespondenzsprache, '])+".tex", "r")
    a = i.read()
    f.write(a)

def tex_escape(text):
    """
        :param text: a plain text message
        :return: the message escaped to appear correctly in LaTeX
    """
    conv = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless{}',
        '>': r'\textgreater{}',
        'ä': r'\"a',
        'ö': r'\"o',
        'ü': r'\"u',
        'Ä': r'\"A',
        'Ö': r'\"O',
        'Ü': r'\"U',
        'ç': r'\c{c}',
        'î': r'\^{\i}',
        'ï': r'\"{\i}',
        'à': r'\`a',
        'è': r'\`e',
        'é': r'\'e',
        ' ': r'',
        'â':'\^{a}',
        'û': '\^{u}',
        'ò': '\`o',
        'ù': '\`u',
    }
    regex = re.compile('|'.join(re.escape(str(key)) for key in sorted(conv.keys(), key = lambda item: - len(item))))
    return regex.sub(lambda match: conv[match.group()], text)


