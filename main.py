# Magic Formula Investing Calculator
#
# Takes a csv or simple list of stocks named "stocks.txt" and looks up info via Y! Finance
# Calculates return on invested capital, enterprise yield, and % change in price (6m and 12m).
# Returns results in csv.
#
# References:
# https://www.investopedia.com/terms/m/magic-formula-investing.asp
# https://www.magicformulainvesting.com/
# https://www.quant-investing.com/strategies/magic-formula-pi-6m
#
# For entertainment purposes only.

import csv
from MagicFormula import MagicFormula
from datetime import datetime, time
import pandas_market_calendars as mcal
from dateutil.relativedelta import relativedelta

def get_last_trading_day():
    nyse = mcal.get_calendar('NYSE')
    early = nyse.schedule(start_date=datetime.now() - relativedelta(days=5), end_date=datetime.now())
    lastday = mcal.date_range(early, frequency='1D')[-1]
    return lastday.date()


last_open = get_last_trading_day()

# will take a csv of tickers, reading the first column as the ticker names
with open('stocks.txt', 'r') as f:
    thingy = [row.split(",")[0] for row in f]

with open('stonk_data.csv', mode='w', newline='') as results:
    resultswriter = csv.writer(results, delimiter=',')
    resultswriter.writerow([
        'date',
        'ticker',
        'return_on_invested_capital',
        'enterprise_yield',
        'price_12m_ago',
        'price_6m_ago',
        'last_price',
        '12m_percent_change',
        '6m_percent_change',
        'marketCap',
        'marketCap_category',
        'ebit',
        'working_capital',
        'netPPE',
        'enterprise_value'
    ])

    for i in thingy:
        magic_object = MagicFormula(i.strip(), last_open)
        try:
            print(magic_object.__str__())
            resultswriter.writerow(magic_object.__str__())
        except:
            magic_object.debug_writer("*** CRITICAL ERROR: Hard fail on ")
