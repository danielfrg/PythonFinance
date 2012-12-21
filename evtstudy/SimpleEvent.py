import numpy as np
import pandas as pd
from scipy import stats
from datetime import datetime
from finance.utils import BasicUtils

class SimpleEvent(object):
    def __init__(self):
        self.data = None
        self.market = None

        self.start_period = None
        self.end_period = None
        self.start_window = None
        self.end_window = None


    def market_return(self):
        # 1. Linear Regression: On the estimation_period
        dr_data = BasicUtils.daily_returns(self.data)
        dr_market = BasicUtils.daily_returns(self.market)
        c_name = dr_data.columns[0]
        x =  dr_market[c_name][self.start_period:self.end_period]
        y = dr_data[c_name][self.start_period:self.end_period]
        slope, intercept, r_value, p_value, std_error = stats.linregress(x, y)
        expected_return = lambda x: x * slope + intercept

        # 2. Analysis on the event window
        # Expexted Return:
        self.er = dr_market[self.start_window:self.end_window].apply(expected_return)[c_name]
        self.er.name = 'Expected Return'
        # Abnormal return: Return of the data - expected return
        self.ar = dr_data[c_name][self.start_window:self.end_window] - self.er
        self.ar.name = 'Abnormal Return'
        # Cumulative abnormal return
        self.car = self.ar.apply(np.cumsum)
        self.car.name = 'Cumulative Abnormal Return'
        # t-test
        t_test_calc = lambda x: x / std_error
        self.t_test = self.car.apply(t_test_calc)
        self.t_test.name = 't test'
        self.prob = self.t_test.apply(stats.norm.cdf)
        self.prob.name = 'Probability'

if __name__ == "__main__":
    from finance.evtstudy import PastEvent
    pevt = PastEvent('./data')
    pevt.symbol = 'AAPL'
    pevt.market = "^gspc"
    pevt.lookback_days = 10
    pevt.lookforward_days = 10
    pevt.estimation_period = 252
    pevt.date = datetime(2009, 1, 5)
    pevt.run()
    print(pevt.er)