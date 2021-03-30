from yahooquery import Ticker
from dateutil.relativedelta import relativedelta


class MagicFormula:

    def __init__(self, ticker, last_open, debug_level=0):
        self.debug = debug_level

        self.ticker = ticker
        self.roic = None
        self.ebit = None
        self.working_cap = None
        self.net_PPE = None
        self.ev = None
        self.ey = None
        self.price_12m = None
        self.price_6m = None
        self.price_now = None
        self.change_12m = None
        self.change_6m = None
        self.market_cap = None
        self.cap_category = None

        self._last_trade_date = last_open

        ### These next three lines are the time consuming part. Once we have this info, we can derive the rest of the
        ### info (except for the change in price over time).

        self._yq = Ticker(ticker)
        self._all_financial_data = self._yq.all_financial_data()
        self._valuation_measures = self._yq.valuation_measures

        try:  # enterprise value
            last_ev = self._valuation_measures[self._valuation_measures['periodType'] == '3M'].tail(1)
            self.ev = float(last_ev.EnterpriseValue)
        except:
            self.debug_writer(2, "WARNING: Failed to get enterprise value for ")

        try:  # market cap
            last_market_cap = self._valuation_measures[self._valuation_measures['periodType'] == '3M'].tail(1)
            self.market_cap = float(last_market_cap.MarketCap)
        except:
            self.debug_writer(2, "WARNING: Failed to get market cap for ")

        try:  # working cap
            self.working_cap = self._all_financial_data.WorkingCapital[-1]
        except:
            self.debug_writer(2, "WARNING: Failed to get working capital for ")

        try:  # net plant, property, and equipment
            self.net_PPE = self._all_financial_data.NetPPE[-1]
        except:
            self.debug_writer(2, "WARNING: Failed to failed to get net PPE for ")

        try:  # expenses before interest and taxes
            self.ebit = self._all_financial_data.EBIT[-1]
        except:
            self.debug_writer(2, "WARNING: Failed to get EBIT for ")

        try:  # ticker price from last year
            date_12m = self._last_trade_date - relativedelta(years=1)
            history = self._yq.history("1d", "1d", date_12m, date_12m + relativedelta(days=1))
            self.price_12m = float(history.close)
        except:
            self.debug_writer(2, "WARNING: Failed to get last year's price for ")

        try:  # ticker price from 6m ago
            date_6m = self._last_trade_date - relativedelta(days=182)
            history = self._yq.history("1d", "1d", date_6m, date_6m + relativedelta(days=1))
            self.price_6m = float(history.close)
        except:
            self.debug_writer(2, "WARNING: Failed to get price from 6m ago for ")

        try:  # last closing price
            history = self._yq.history("1d", "1d", self._last_trade_date).tail(1)
            self.price_now = float(history.close)
        except:
            self.debug_writer(2, "WARNING: Failed to get last trading day price for ")

        ### Run calculations
        # ROIC (Return on invested capital) = EBIT / (net working capital + net PPE)
        if self.ebit and self.working_cap and self.net_PPE:
            self.roic = self.ebit / (self.working_cap + self.net_PPE)
        else:
            self.debug_writer(2, "WARNING: Could not calculate return on invested capital for ")

        # Earnings yield = EBIT / Enterprise value
        if self.ebit and self.ev:
            self.ey = self.ebit / self.ev
        else:
            self.debug_writer(2, "WARNING: Could not calculate enterprise yield for ")

        # 12m change in price
        if self.price_now and self.price_12m and self.price_12m != 0:
            self.change_12m = ((self.price_now - self.price_12m) / self.price_12m)
        else:
            self.debug_writer(2, "WARNING: Could not calculate change in previous 12m price for ")

        # 6m change in price
        if self.price_now and self.price_6m and self.price_6m != 0:
            self.change_6m = ((self.price_now - self.price_6m) / self.price_6m)
        else:
            self.debug_writer(2, "WARNING: Could not calculate change in previous 6m price for ")

        ### Categorize market cap for easy excel grouping
        if self.market_cap:
            self.cap_category = "nano"
            if self.market_cap >= 50000000:
                self.cap_category = "micro"
            if self.market_cap >= 300000000:
                self.cap_category = "small"
            if self.market_cap >= 2000000000:
                self.cap_category = "medium"
            if self.market_cap >= 10000000000:
                self.cap_category = "large"
            if self.market_cap >= 200000000000:
                self.cap_category = "mega"
        self.debug_writer(3, "INFO: Finished getting info for ")

    def debug_writer(self, message_debug_level, message):
        if self.debug >= message_debug_level:
            print(message, self.ticker)

    def __str__(self):
        return [
            str(self._last_trade_date),
            str(self.ticker),
            str(self.roic),
            str(self.ey),
            str(self.price_12m),
            str(self.price_6m),
            str(self.price_now),
            str(self.change_12m),
            str(self.change_6m),
            str(self.market_cap),
            str(self.cap_category),
            str(self.ebit),
            str(self.working_cap),
            str(self.net_PPE),
            str(self.ev)
        ]

    def __repr__(self):
        return [
            self._last_trade_date,
            self.ticker,
            self.roic,
            self.ey,
            self.price_12m,
            self.price_6m,
            self.price_now,
            self.change_12m,
            self.change_6m,
            self.market_cap,
            self.cap_category,
            self.ebit,
            self.working_cap,
            self.net_PPE,
            self.ev
        ]
