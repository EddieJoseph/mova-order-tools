import math
from datetime import datetime
import numpy as np
import pandas as pd



def initialize(overall: pd.DataFrame, groups: pd.DataFrame):
    overall[['Einheitsnummer','KüchenId','Einheitsname','Stufe','% Level','Budget']] = groups[groups.Einheitsnummer.notnull()][['Einheitsnummer','KüchenId (K_Haupteinheitsnummer)','Einheitsname','Stufe','% Level','Essensbudget pro Einheit']]
    overall['Personen'] = groups[groups.Einheitsnummer.notnull()]['Anzahl Teilnehmende'] + groups[groups.Einheitsnummer.notnull()]['Anzahl Leitende']
    overall['Personen gewichtet'] = groups[groups.Einheitsnummer.notnull()]['Anzahl Teilnehmende'] * groups[groups.Einheitsnummer.notnull()]['% Level'] + groups[groups.Einheitsnummer.notnull()]['Anzahl Leitende']
    overall['Tage'] = np.sign(groups[groups.Einheitsnummer.notnull()][[datetime(2022, 7, 23),datetime(2022, 7, 24),datetime(2022, 7, 25),datetime(2022, 7, 26),datetime(2022, 7, 27),datetime(2022, 7, 28),datetime(2022, 7, 29),datetime(2022, 7, 30),datetime(2022, 7, 31),datetime(2022, 8, 1),datetime(2022, 8, 2),datetime(2022, 8, 3),datetime(2022, 8, 4),datetime(2022, 8, 5),datetime(2022, 8, 6)]]).sum(axis=1)

#
def cost(overall: pd.DataFrame, orders: pd.DataFrame):
    for nr in overall['Einheitsnummer'].tolist():
        # print(sum(orders[(orders.Einheitsnummer == nr)]['OrderQtyInCU']*orders[(orders.Einheitsnummer == nr)]['OrderPriceInCU']))
        overall.loc[overall['Einheitsnummer'] == nr, 'Kosten'] = sum(orders[(orders.Einheitsnummer == nr)]['OrderQtyInCU']*orders[(orders.Einheitsnummer == nr)]['OrderPriceInCU'])

    overall['Differnenz'] = overall['Budget']-overall['Kosten']

def breakfast(overall: pd.DataFrame, orders: pd.DataFrame):
    tmp = orders[orders.Number == 'MIG111013000000']
    for nr in overall['Einheitsnummer'].tolist():
        overall.loc[overall['Einheitsnummer'] == nr, 'Brot kg'] = sum(tmp[(tmp.Einheitsnummer == nr)]['OrderQtyInCU']*tmp[(tmp.Einheitsnummer == nr)]['OrderSizeKGL'])

        tempd = tmp[tmp.MenuPlanDate == datetime(2022, 7, 24)]
        overall.loc[overall['Einheitsnummer'] == nr, 'Brot kg erster Tag'] = sum(
        tempd[(tempd.Einheitsnummer == nr)]['OrderQtyInCU'] * tempd[(tempd.Einheitsnummer == nr)]['OrderSizeKGL'])


    overall['Brot kg pro g.Person und Tag'] = overall['Brot kg'] / overall['Personen gewichtet'] / overall['Tage']

    tmp = orders[orders.Number == 'MIG204242000000']
    for nr in overall['Einheitsnummer'].tolist():
        overall.loc[overall['Einheitsnummer'] == nr, 'Butter kg'] = sum(tmp[(tmp.Einheitsnummer == nr)]['OrderQtyInCU']*tmp[(tmp.Einheitsnummer == nr)]['OrderSizeKGL'])

        # tempd = tmp[tmp.MenuPlanDate == datetime(2022, 7, 24)]
        # print('2')
        # print(tempd)
        # overall.loc[overall['Einheitsnummer'] == nr, 'Butter kg erster Tag'] = sum(tempd[(tempd.Einheitsnummer == nr)]['OrderQtyInCU']*tempd[(tempd.Einheitsnummer == nr)]['OrderSizeKGL'])

    overall['Butter kg pro g.Person erste Bestellung'] = overall['Butter kg'] / overall['Personen gewichtet']

    tmp = orders[orders.Number == 'MIG204014000000']
    for nr in overall['Einheitsnummer'].tolist():
        overall.loc[overall['Einheitsnummer'] == nr, 'Milch l'] = sum(tmp[(tmp.Einheitsnummer == nr)]['OrderQtyInCU']*tmp[(tmp.Einheitsnummer == nr)]['OrderSizeKGL'])
    overall['Milch l pro g.Person und Tag'] = overall['Milch l'] / overall['Personen gewichtet'] / overall['Tage']





def days(overall: pd.DataFrame, orders: pd.DataFrame, groups: pd.DataFrame):
    for date in [datetime(2022, 7, 23),datetime(2022, 7, 24),datetime(2022, 7, 25),datetime(2022, 7, 26),datetime(2022, 7, 27),datetime(2022, 7, 28),datetime(2022, 7, 29),datetime(2022, 7, 30),datetime(2022, 7, 31),datetime(2022, 8, 1),datetime(2022, 8, 2),datetime(2022, 8, 3),datetime(2022, 8, 4),datetime(2022, 8, 5),datetime(2022, 8, 6)]:
        tmp1 = orders[orders.MenuPlanDate == date]
        for nr in overall['Einheitsnummer'].tolist():
            if groups[groups.Einheitsnummer.notnull()][groups.Einheitsnummer == nr][date].iloc[0]>0 :
                pg = overall[overall['Einheitsnummer'] == nr]['Personen gewichtet'].iloc[0]
                overall.loc[overall['Einheitsnummer'] == nr, 'Tages Kosten pro g.Person ' + str(date)] = sum(
                    tmp1[(tmp1.Einheitsnummer == nr)]['OrderQtyInCU'] * tmp1[(tmp1.Einheitsnummer == nr)][
                        'OrderPriceInCU'] )/ pg
#            else:
#                overall.loc[overall['Einheitsnummer'] == nr, 'Tages Kosten pro g.Person ' + str(date)] = -1

    for date in [datetime(2022, 7, 23),datetime(2022, 7, 24),datetime(2022, 7, 25),datetime(2022, 7, 26),datetime(2022, 7, 27),datetime(2022, 7, 28),datetime(2022, 7, 29),datetime(2022, 7, 30),datetime(2022, 7, 31),datetime(2022, 8, 1),datetime(2022, 8, 2),datetime(2022, 8, 3),datetime(2022, 8, 4),datetime(2022, 8, 5),datetime(2022, 8, 6)]:
        tmp1 = orders[orders.MenuPlanDate == date]
        for nr in overall['Einheitsnummer'].tolist():
            if groups[groups.Einheitsnummer.notnull()][groups.Einheitsnummer == nr][date].iloc[0]>0 :
                pg = overall[overall['Einheitsnummer'] == nr]['Personen gewichtet'].iloc[0]
                overall.loc[overall['Einheitsnummer'] == nr, 'Tages Menge pro g.Person in kg ' + str(date)] = sum(
                    tmp1[(tmp1.Einheitsnummer == nr)]['OrderQtyInCU'] * tmp1[(tmp1.Einheitsnummer == nr)][
                        'OrderSizeKGL'] )/ pg
#            else:
#                overall.loc[overall['Einheitsnummer'] == nr, 'Tages Menge pro g.Person in kg ' + str(date)] = -1


    # MIG111013000000 Ruchbrot
    # MIG204242000000 Butter
    # MIG204014000000 Milch


def run_analysis(groups, orders):
    overall = pd.DataFrame()
    # dayli = pd.DataFrame()

    initialize(overall, groups)
    cost(overall,orders)
    breakfast(overall, orders)

    days(overall, orders, groups)


    # print(overall)
    overall.to_excel('Gesamtalyse.xlsx')




