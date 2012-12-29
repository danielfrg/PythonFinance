import numpy as np
import pandas as pd
from datetime import datetime

from finance.utils import DateUtils
from finance.utils import DataAccess
from finance.events.EventStudy import EventStudy

class PastEvent(EventStudy):
    '''
    Analyse a particular equity on a particular date
    
    Necesary Parameters
    -------------------
        date: datetime
        symbol: str, eg: AAPL
    
    Optional Parameters
    -------------------
        market: str, default2-'SPY' - used to asses the event
        lookback_days: int, default=20 - past event window size
        lookforward_days: int, default=20 - future event window size
        estimation_period: int, default=255

    |-----255-----|-------20-------|-|--------20--------|
       estimation      lookback   event   lookforward
    '''

    def __init__(self, path='./data'):
        # Utils
        self.data_access = DataAccess(path)

        # Variables
        self.date = None # Date of the event
        self.symbol = None
        self.field = 'Adj Close'
        self.lookback_days = 20
        self.lookforward_days = 20
        self.estimation_period = 255
        self.market = "SPY"

        # Results
        self.evt_window_data = None
        self.er = None
        self.ar = None
        self.car = None
        self.t_test = None
        self.prob = None


    def run(self):
        dates = DateUtils.nyse_dates_event(self.date,
                            self.lookback_days, self.lookforward_days, self.estimation_period)
        start_date = dates[0]
        end_date = dates[-1]

        # Data to the General market_return Study
        self.data = self.data_access.get_data(self.symbol, start_date, end_date, self.field)
        evt_window_dates = dates[- self.lookforward_days - self.lookback_days - 1:]
        self.evt_window_data = self.data[evt_window_dates[0]:dates[-1]]
        self.market = self.data_access.get_data(self.market, start_date, end_date, self.field)
        # Parameters of the General market_return Study
        self.start_period = dates[0]
        self.end_period = dates[self.estimation_period]
        self.start_window = dates[self.estimation_period]
        self.end_window = dates[-1]

        # Run the Market Return method
        super().market_return()