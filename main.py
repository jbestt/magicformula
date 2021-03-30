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
from Writer import Writer
import concurrent.futures

def get_last_trading_day():
    nyse = mcal.get_calendar('NYSE')
    early = nyse.schedule(start_date=datetime.now() - relativedelta(days=5), end_date=datetime.now())
    lastday = mcal.date_range(early, frequency='1D')[-1]
    return lastday.date()

def ticker_wrapper(ticker, debug_level, last_open, resultswriter):
    magic_object = MagicFormula(ticker, debug_level, last_open)
    try:
        print(magic_object.__str__())
        resultswriter.write_row(magic_object.__str__())
    except:
        magic_object.debug_writer(0, "*** CRITICAL FAILURE: Failure on ticker ")


last_open = get_last_trading_day()

sourcefile = 'stocks.txt'
destfile = 'stonk_data.csv'
threads = 10

###     Debug Levels:
#       0 = Critical
#       1 = Error
#       2 = Warn
#       3 = Info
debug_level = 2

header = [
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
    ]

# will take a csv of tickers, reading the first column as the ticker names
with open(sourcefile, 'r') as f:
    tickers = [row.split(",")[0] for row in f]

writer = Writer(destfile, header)

# now with threads! thanks wedgie
with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
    for i in tickers:
        executor.submit(ticker_wrapper, i.strip(), debug_level, last_open, writer)