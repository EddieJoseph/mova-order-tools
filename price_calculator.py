import pandas as pd


def generate_price_report(orders: pd.DataFrame, groups: pd.DataFrame, prices: pd.DataFrame):
    kitchens = expand_kids(groups)

    current_price = []
    KID = []
    for index, row in orders.iterrows():
        try:
            if (prices[prices['Number'] == row['Number']]['Preisart'].values[0] == "CU"):
                current_price.append(prices[prices['Number'] == row['Number']]['OrderPriceInCU'].values[0])
            else:
                current_price.append(
                    prices[prices['Number'] == row['Number']]['OrderPriceInCU'].values[0] * row['OrderSizeKGL'])
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

    kitchen_cost_per_day = calculate_daily_prices(orders, kitchens)
    kitchen_cost_per_day.to_excel('Tageskosten.xlsx', index=False)


def expand_kids(groups:pd.DataFrame):
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

    kids_num = []
    haupteinheitnummer = []
    kontakt = []
    gesamtzahl = []
    gesamtzahl_internationale = []
    haupteinheitsname = []
    butget = []
    einheitsnummern = []
    startdaten = []
    enddaten = []
    language = []

    for index, row in kitchens.iterrows():
        groups_in_kitchen = groups[groups['KüchenId, '] == row['KüchenId, ']]
        kids_num.append(int(str(row['KüchenId, '])[2:]))
        bigger = groups_in_kitchen[groups_in_kitchen['Budget'] == groups_in_kitchen['Budget'].max()]
        haupteinheitnummer.append(bigger['Einheitsnummer, '].values[0])
        haupteinheitsname.append(bigger['Einheitsname,'].values[0])
        kontakt.append(bigger['E-Mailadresse (Stand März22)'].values[0])
        gesamtzahl.append(groups_in_kitchen['Gesamtzahl Einheit, '].sum())
        gesamtzahl_internationale.append(groups_in_kitchen['Gesamtzahl Internationale Einheit, '].sum())
        butget.append(groups_in_kitchen['Budget'].sum())
        startdaten.append(groups_in_kitchen['Startdatum'].min())
        enddaten.append(groups_in_kitchen['Enddatum'].max())
        language.append(bigger['Sprache, '].values[0])
        numbers = ""
        for iindex, ivalue in groups_in_kitchen['Einheitsnummer, '].items():
            numbers = numbers + str(ivalue) + ', '
        einheitsnummern.append(numbers[0:-2])

    kitchens['KüchenId_Num'] = kids_num
    kitchens['haupteinheitnummer'] = haupteinheitnummer
    kitchens['Korrespondenzsprache'] = language
    kitchens['einheitsnummern'] = einheitsnummern
    kitchens['Haupteinheitsname'] = haupteinheitsname
    kitchens['kontakt'] = kontakt
    kitchens['Gesamtzahl'] = gesamtzahl
    kitchens['Gesamtzahl_internationale'] = gesamtzahl_internationale
    kitchens['Butget'] = butget
    kitchens['Startdatum'] = startdaten
    kitchens['Enddatum'] = enddaten
    return kitchens.sort_values(by=['KüchenId_Num'])




def calculate_daily_prices(orders: pd.DataFrame, kitchens: pd.DataFrame):
    for date in pd.date_range('2022-07-23', '2022-08-06', freq='1d'):
        orders_day = orders[orders['MenuPlanDate'] == date]
        cost_day = [];
        for index, row in kitchens.iterrows():
            cost_day.append(orders_day[orders_day['KID'] == row['KüchenId, ']]['Cost'].sum())
        kitchens[date] = cost_day
    return kitchens
