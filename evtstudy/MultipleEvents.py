import numpy as np
import pandas as pd
from scipy import stats
from datetime import datetime
from finance.utils import DateUtils
from finance.utils import DataAccess
from finance.utils import BasicUtils

class MultipleEvents(object):
    def __init__(self, path='./data/'):
        self.path = path
        self.data_access = DataAccess(path)

        self.matrix = None
        self.market = 'SPY'
        self.lookback_days = 20
        self.lookforward_days = 20
        self.estimation_period = 100
        self.field = 'Adj Close'

        # Result
        self.data_window = None
        self.data_estimation = None
        self.market_window = None
        self.market_estimation = None

        self.dr_data_window = None
        self.dr_data_estimation = None
        self.dr_market_window = None
        self.dr_market_estimation = None

        self.expected_returns = None
        self.abnormal_returns = None

    def run(self):
        '''
        Assess the events

        Prerequisites
        -------------
            self.matrix
            self.market = 'SPY'
            self.lookback_days = 20
            self.lookforward_days = 20
            self.estimation_period = 100
            self.field = 'Adj Close'
        '''
        # 0. Get the dates and Download/Import the data
        # |-----100----|----20-------|-|--------20--------|
        #   estimation    lookback  event    lookforward

        symbols = self.matrix.columns
        start_date = self.matrix.index[0]
        end_date = self.matrix.index[-1]
        nyse_dates = DateUtils.nyse_dates(start=start_date, end=end_date,
                        lookbackDays=self.lookback_days + self.estimation_period,
                        lookforwardDays=self.lookforward_days, list=True)
        data = self.data_access.get_data(symbols, nyse_dates[0], nyse_dates[-1], self.field)
        market = self.data_access.get_data(self.market, nyse_dates[0], nyse_dates[-1], self.field)

        # 1. Create DataFrames with the data of each event
        evt_window_dic = {}
        evt_estimation_dic = {}
        market_window_dic = {}
        market_estimation_dic = {}
        for symbol in symbols:
            for (item, i) in zip(self.matrix[symbol], range(len(self.matrix))):
                if item == 1:
                    col_name = symbol + ' ' + self.matrix.index[i].to_pydatetime().strftime('%Y-%m-%d')
                    evt_idx = i + self.estimation_period + self.lookback_days # event idx on self.data
                    # 1.1 Data on the event window: self.evt_windows_data
                    start_idx = evt_idx - self.lookback_days # window start idx on self.data
                    end_idx = evt_idx + self.lookforward_days + 1 # window end idx on self.data
                    data_window = data[symbol][start_idx:end_idx]
                    data_window.index = range(- self.lookback_days, self.lookforward_days + 1)
                    evt_window_dic[col_name] = data_window
                    # 1.2 Market on the event window: self.market_window
                    market_window = market[self.field][start_idx:end_idx]
                    market_window.index = range(- self.lookback_days, self.lookforward_days + 1)
                    market_window_dic[col_name] = market_window

                    # 1.3 Data on the estimation period: self.data_estimation
                    start_idx = evt_idx - self.lookback_days - self.estimation_period # estimation start idx on self.data
                    end_idx = evt_idx - self.lookback_days # estimation end idx on self.data
                    data_estimation = data[symbol][start_idx:end_idx]
                    data_estimation.index = range(-self.estimation_period - self.lookback_days,
                                                    - self.lookback_days)
                    evt_estimation_dic[col_name] = data_estimation
                    # 1.4 Market on the estimation period: self.market_estimation
                    market_estimation = market[self.field][start_idx:end_idx]
                    market_estimation.index = range(-self.estimation_period - self.lookback_days,
                                                    - self.lookback_days)
                    market_estimation_dic[col_name] = market_estimation
        # 1.5 Create pd.DataFrames with the dictionaries
        self.data_window = pd.DataFrame(evt_window_dic)
        self.data_estimation = pd.DataFrame(evt_estimation_dic)
        self.market_window = pd.DataFrame(market_window_dic)
        self.market_estimation = pd.DataFrame(market_estimation_dic)

        # 2. Assess the data
        # 2.1 Calculate the daily returns
        self.dr_data_window = BasicUtils.daily_returns(self.data_window)
        self.dr_data_estimation = BasicUtils.daily_returns(self.data_estimation)
        self.dr_market_window = BasicUtils.daily_returns(self.market_window)
        self.dr_market_estimation = BasicUtils.daily_returns(self.market_estimation)
        # 2.2 Calculate: regression, expected return
        reg_estimation = pd.DataFrame(index=self.dr_market_estimation.columns,
                                        columns=['Intercept', 'Slope', 'Std Error'])
        self.expected_returns = pd.DataFrame(index=self.dr_market_window.index,
                                        columns=self.dr_market_window.columns)
        # For each column (event) on the estimation period
        for col in self.dr_market_estimation.columns:
            # 2.1 Calculate the regression
            x = self.dr_data_estimation[col]
            y = self.dr_market_estimation[col]
            slope, intercept, r_value, p_value, slope_std_error = stats.linregress(x, y)
            reg_estimation['Slope'][col] = slope
            reg_estimation['Intercept'][col] = intercept
            reg_estimation['Std Error'][col] = slope_std_error
            # 2.2 Calculate the expected return of each date using the regression
            expected_return = lambda x: x * slope + intercept
            self.expected_returns[col] = self.dr_market_window[col].apply(expected_return)

        # 3.
        self.abnormal_returns = self.dr_data_window - self.expected_returns
        self.abnormal_return = self.abnormal_returns.sum(axis=1)

if __name__ == '__main__':
    from finance.evtstudy import EventFinder
    evtf = EventFinder('./data')
    evtf.symbols = ['AAPL', 'GOOG', 'XOM']
    evtf.start_date = datetime(2009, 1, 1)
    evtf.end_date = datetime(2011, 1, 1)
    evtf.function = evtf.increase(10)
    evtf.search()
    print(evtf.num_events)

    mevt = MultipleEvents('./data')
    mevt.matrix = evtf.matrix
    mevt.market = 'SPY'
    mevt.lookback_days = 10
    mevt.lookforward_days = 10
    mevt.estimation_period = 50
    mevt.run()

    import matplotlib.pyplot as plt
    mevt.abnormal_return.plot()
    plt.show()