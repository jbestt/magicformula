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

from MagicFormula import MagicFormula
from datetime import datetime, time
import pandas_market_calendars as mcal
from dateutil.relativedelta import relativedelta
from Writer import Writer
import concurrent.futures


def get_last_trading_day() -> datetime:
    nyse = mcal.get_calendar('NYSE')
    early = nyse.schedule(start_date=datetime.now() - relativedelta(days=5), end_date=datetime.now())
    lastday = mcal.date_range(early, frequency='1D')[-1]
    return lastday.date()


def tickler_wrapper(tickler: str, last_open: datetime, resultswriter: Writer, debug_level=0):
    magic_object = MagicFormula(tickler, last_open, debug_level)
    try:
        print(magic_object.__str__())
        resultswriter.write_row(magic_object.__str__())
    except:
        magic_object.debug_writer(0, "*** CRITICAL FAILURE: Failure on tickler ")


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
    'tickler',
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

last_open = get_last_trading_day()

# Will take a csv of ticklers, reading the first column as the tickler names.
with open(sourcefile, 'r') as f:
    ticklers = [row.split(",")[0] for row in f]

writer = Writer(destfile, header)

# Now with threads! Thanks wedgie.
with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
    for i in ticklers:
        executor.submit(tickler_wrapper, i.strip(), last_open, writer, debug_level)
