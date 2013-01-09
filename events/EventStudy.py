import numpy as np
import pandas as pd
from scipy import stats
from datetime import datetime
from finance.utils import Calculator

class EventStudy(object):
    def __init__(self):
        self.data = None
        self.market = None

        self.start_period = None
        self.end_period = None
        self.start_window = None
        self.end_window = None


    def market_return(self):
        # 1. Linear Regression: On the estimation_period
        dr_data = Calculator.returns(self.data)
        dr_market = Calculator.returns(self.market)
        c_name = dr_data.columns[0]
        x =  dr_market[c_name][self.start_period:self.end_period]
        y = dr_data[c_name][self.start_period:self.end_period]
        slope, intercept, r_value, p_value, std_error = stats.linregress(x, y)
        er = lambda x: x * slope + intercept

        # 2. Analysis on the event window
        # Expexted Return:
        self.er = dr_market[self.start_window:self.end_window].apply(er)[c_name]
        self.er.name = 'Expected return'
        # Abnormal return: Return of the data - expected return
        self.ar = dr_data[c_name][self.start_window:self.end_window] - self.er
        self.ar.name = 'Abnormal return'
        # Cumulative abnormal return
        self.car = self.ar.cumsum()
        self.car.name = 'Cum abnormal return'
        # t-test
        t_test_calc = lambda x: x / std_error
        self.t_test = self.ar.apply(t_test_calc)
        self.t_test.name = 't-test'
        self.prob = self.t_test.apply(stats.norm.cdf)
        self.prob.name = 'Probability'