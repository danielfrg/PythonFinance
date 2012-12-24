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
        self.estimation_period = 200
        self.field = 'Adj Close'

        # Result
        self.equities_window = None
        self.equities_estimation = None
        self.market_window = None
        self.market_estimation = None

        self.reg_estimation = None

        self.dr_equities_window = None
        self.dr_equities_estimation = None
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
            self.estimation_period = 200
            self.field = 'Adj Close'
        '''
        # 0. Get the dates and Download/Import the data
        # |-----100-----|-------20-------|-|--------20--------|
        #   estimation       lookback   event   lookforward

        symbols = self.matrix.columns
        start_date = self.matrix.index[0]
        end_date = self.matrix.index[-1]

        nyse_dates = DateUtils.nyse_dates(start=start_date, end=end_date,
                        lookbackDays=self.lookback_days + self.estimation_period + 1,
                        lookforwardDays=self.lookforward_days, list=True)
        data = self.data_access.get_data(symbols, nyse_dates[0], nyse_dates[-1], self.field)
        if len(data.columns) == 1:
            data.columns = symbols
        market = self.data_access.get_data(self.market, nyse_dates[0], nyse_dates[-1], self.field)
        print(data.index[0], data.index[-1])

        # 1. Create DataFrames with the data of each event
        windows_indexes = range(- self.lookback_days, self.lookforward_days + 1)
        estimation_indexes = range(-self.estimation_period - self.lookback_days - 1, - self.lookback_days)
        self.equities_window = pd.DataFrame(index=windows_indexes)
        self.market_window = pd.DataFrame(index=windows_indexes)
        self.equities_estimation = pd.DataFrame(index=estimation_indexes)
        self.market_estimation = pd.DataFrame(index=estimation_indexes)
        for symbol in symbols:
            for (item, i) in zip(self.matrix[symbol], range(len(self.matrix))):
                if item == 1: # Event marked on the matrix
                    col_name = symbol + ' ' + self.matrix.index[i].to_pydatetime().strftime('%Y-%m-%d')
                    evt_idx = i + self.estimation_period + self.lookback_days + 1 # event idx on self.data

                    # 1.1 Equities on the event window: self.evt_windows_data
                    start_idx = evt_idx - self.lookback_days # window start idx on self.data
                    end_idx = evt_idx + self.lookforward_days + 1 # window end idx on self.data
                    new_equities_window = data[symbol][start_idx:end_idx]
                    new_equities_window.index = self.equities_window.index
                    self.equities_window[col_name] = new_equities_window

                    # 1.2 Market on the event window: self.market_window
                    new_market_window = market[self.field][start_idx:end_idx]
                    new_market_window.index = self.market_window.index
                    self.market_window[col_name] = new_market_window

                    # 1.3 Data on the estimation period: self.equities_estimation
                    start_idx = evt_idx - self.lookback_days - self.estimation_period - 1# estimation start idx on self.data
                    end_idx = evt_idx - self.lookback_days # estimation end idx on self.data
                    new_equities_estimation = data[symbol][start_idx:end_idx]
                    new_equities_estimation.index = self.equities_estimation.index
                    self.equities_estimation[col_name] = new_equities_estimation

                    # 1.4 Market on the estimation period: self.market_estimation
                    new_market_estimation = market[self.field][start_idx:end_idx]
                    new_market_estimation.index = self.market_estimation.index
                    self.market_estimation[col_name] = new_market_estimation

        '''
        # 2. Assess the data
        # 2.1 Calculate the daily returns
        self.dr_equities_window = BasicUtils.daily_returns(self.equities_window)
        self.dr_equities_estimation = BasicUtils.daily_returns(self.equities_estimation)
        self.dr_market_window = BasicUtils.daily_returns(self.market_window)
        self.dr_market_estimation = BasicUtils.daily_returns(self.market_estimation)
        # 2.2 Calculate: regression, expected return
        self.reg_estimation = pd.DataFrame(index=self.dr_market_estimation.columns,
                                        columns=['Intercept', 'Slope', 'Std Error'])
        self.expected_returns = pd.DataFrame(index=self.dr_market_window.index,
                                        columns=self.dr_market_window.columns)
        # For each column (event) on the estimation period
        for col in self.dr_market_estimation.columns:
            # 2.1 Calculate the regression
            x = self.dr_market_estimation[col]
            y = self.dr_equities_estimation[col]
            slope, intercept, r_value, p_value, slope_std_error = stats.linregress(x, y)
            self.reg_estimation['Slope'][col] = slope
            self.reg_estimation['Intercept'][col] = intercept
            self.reg_estimation['Std Error'][col] = slope_std_error
            # 2.2 Calculate the expected return of each date using the regression
            self.expected_returns[col] = intercept + self.dr_market_window[col] * slope

        # 3. Final calculations
        self.abnormal_returns = self.dr_equities_window - self.expected_returns
        self.abnormal_return = self.abnormal_returns.mean(axis=1)
        self.cumulative_abnormal_returns = self.abnormal_returns.apply(np.cumsum)
        self.cumulative_abnormal_return = self.cumulative_abnormal_returns.mean(axis=1)
        #'''

if __name__ == '__main__':
    from finance.evtstudy import EventFinder
    evtf = EventFinder('./data')
    evtf.symbols = ['AMD']
    evtf.start_date = datetime(2008, 1, 1)
    evtf.end_date = datetime(2008, 10, 28)
    evtf.function = evtf.went_below(3)
    evtf.search()
    #print(evtf.num_events)

    mevt = MultipleEvents('./data')
    mevt.matrix = evtf.matrix
    mevt.market = 'SPY'
    mevt.lookback_days = 20
    mevt.lookforward_days = 20
    mevt.estimation_period = 200
    mevt.run()

    #print(mevt.dr_market_window)
    #print(mevt.reg_estimation.ix[0])
    #print(mevt.equities_window)

    import matplotlib.pyplot as plt
    from scipy import linspace
    #mevt.cumulative_abnormal_return.plot()
    #plt.show()