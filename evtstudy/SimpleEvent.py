import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from datetime import datetime
from finance.utils import BasicUtils as bu

class SimpleEvent(object):
    def __init__(self, path='./data'):
        self.data = None
        self.market = None

        self.start_period = None
        self.end_period = None
        self.start_window = None
        self.end_window = None


    def market_return(self):
        # 1. Regression: On the period before the window
        dr_data = bu.daily_returns(self.data)
        dr_market = bu.daily_returns(self.market)
        dr_market['intercept'] = 1
        reg_results = sm.OLS(dr_data[self.start_period:self.end_period],
                        dr_market[self.start_period:self.end_period]).fit()
        del dr_market['intercept']
        # Solution to the regresion
        slope = reg_results.params[0]
        intercept = reg_results.params[1]
        std_error = dr_market[self.start_period:self.end_period].std()['Daily Return']
        expected_return = lambda x: x * slope + intercept

        # 2. Analysis on the event window
        # Expexted Return:
        self.er = dr_market['Daily Return'][self.start_window:self.end_window].apply(expected_return)
        self.er.name = 'Expected Return'
        # Abnormal return: Return of the data - expected return
        self.ar = dr_data['Daily Return'][self.start_window:self.end_window] - self.er
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

