import pandas as pd


def generate_price_report(orders: pd.DataFrame, groups: pd.DataFrame, prices: pd.DataFrame):
    kitchens = expand_kids(groups)

    current_price = []
    KID = []
    for index, row in orders.iterrows():
        try:
            current_price.append(prices[prices['Number'] == row['Number']]['OrderPriceInCU'].values[0])
        except:
            print('Price missing', row['Number'], index)
            current_price.append(0)
        try:
            KID.append(groups[groups['Einheitsnummer, '] == row['Einheitsnummer']]['KüchenId, '].values[0])
        except:
            print('Group not found',row['Einheitsnummer'])
            KID.append('NaN')
    orders['CurrentPriceCU'] = current_price
    orders['KID'] = KID
    orders['Cost'] = orders['OrderQytCU'] * orders['CurrentPriceCU']

    # print(current_price)
    kitchen_cost_per_day = calculate_daily_prices(orders, kitchens)
    kitchen_cost_per_day.to_excel('Tageskosten.xlsx')



# MIG111013000000
def expand_kids(groups:pd.DataFrame):
    print()

    startdate = []
    enddate = []
    days = []
    for index, row in groups.iterrows():
        start = pd.to_datetime(row['Datum Lager'].split("-")[0],format='%d.%m.%Y')
        end = pd.to_datetime(row['Datum Lager'].split("-")[1],format='%d.%m.%Y')
        startdate.append(start)
        enddate.append(end)
        days.append((end-start).days)

    groups['Startdatum'] = startdate
    groups['Enddatum'] = enddate
    groups['Tage'] = days
    groups['Budget'] = (groups['Gesamtzahl Einheit, ']+groups['Gesamtzahl Internationale Einheit, ']) * (groups['Tage']) * 8 + groups['Anzahl Besuchende'] * 2.5

    kitchens = pd.DataFrame(groups['KüchenId, '].drop_duplicates())

    haupteinheitnummer = []
    kontakt = []
    gesamtzahl = []
    gesamtzahl_internationale = []
    haupteinheitsname = []
    butget = []

    for index, row in kitchens.iterrows():
        groups_in_kitchen = groups[groups['KüchenId, '] == row['KüchenId, ']]
        bigger = groups_in_kitchen[groups_in_kitchen['Budget'] == groups_in_kitchen['Budget'].max()]
        haupteinheitnummer.append(bigger['Einheitsnummer, '].values[0])
        haupteinheitsname.append(bigger['Einheitsname,'].values[0])
        kontakt.append(bigger['E-Mailadresse (Stand März22)'].values[0])
        gesamtzahl.append(groups_in_kitchen['Gesamtzahl Einheit, '].sum())
        gesamtzahl_internationale.append(groups_in_kitchen['Gesamtzahl Internationale Einheit, '].sum())
        butget.append(groups_in_kitchen['Budget'].sum())
    kitchens['haupteinheitnummer'] = haupteinheitnummer
    kitchens['Haupteinheitsname'] = haupteinheitsname
    kitchens['kontakt'] = kontakt
    kitchens['Gesamtzahl'] = gesamtzahl
    kitchens['Gesamtzahl_internationale'] = gesamtzahl_internationale
    kitchens['Butget'] = butget

    # kitchens.to_excel('Küchenaggregation.xlsx')
    return kitchens




def calculate_daily_prices(orders: pd.DataFrame, kitchens: pd.DataFrame):
    for date in pd.date_range('2022-07-23', '2022-08-06', freq='1d'):
        orders_day = orders[orders['MenuPlanDate'] == date]
        cost_day = [];
        for index, row in kitchens.iterrows():

            # print(orders_day['KID'])
            print(row['KüchenId, '])

            cost_day.append(orders_day[orders_day['KID'] == row['KüchenId, ']]['Cost'].sum())
        kitchens[date] = cost_day
    return kitchens
