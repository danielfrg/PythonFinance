import numpy as np
import pandas as pd
from scipy import stats
from datetime import datetime
import matplotlib.pyplot as plt
from finance.plots.errorfill import *

from finance.utils import DateUtils
from finance.utils import DataAccess
from finance.utils import Calculator

class MultipleEvents(object):
    def __init__(self):
        self.data_access = DataAccess()

        self.list = None
        self.market = 'SPY'
        self.lookback_days = 20
        self.lookforward_days = 20
        self.estimation_period = 200
        self.field = 'adjusted_close'

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

        self.er = None
        self.ar = None
        self.car = None

    def run(self):
        '''
        Assess the events

        |-----100-----|-------20-------|-|--------20--------|
           estimation      lookback   event   lookforward

        Prerequisites
        -------------
            self.matrix
            self.market = 'SPY'
            self.lookback_days = 20
            self.lookforward_days = 20
            self.estimation_period = 200
            self.field = 'adjusted_close'
        '''
        # 0. Get the dates and Download/Import the data
        symbols = list(set(self.list))
        start_date = self.list.index[0]
        end_date = self.list.index[-1]
        nyse_dates = DateUtils.nyse_dates(start=start_date, end=end_date,
                        lookbackDays=self.lookback_days + self.estimation_period + 1,
                        lookforwardDays=self.lookforward_days)

        data = self.data_access.get_data(symbols, nyse_dates[0], nyse_dates[-1], self.field)
        market = self.data_access.get_data(self.market, nyse_dates[0], nyse_dates[-1], self.field)

        if len(data.columns) == 1:
            data.columns = symbols
        if len(data) > len(market):
            market = market.reindex(data.index)
            market.columns = [self.field]

        data = data.fillna(method='ffill').fillna(method='bfill')
        market = market.fillna(method='ffill').fillna(method='bfill')

        # 1. Create DataFrames with the data of each event
        windows_indexes = range(- self.lookback_days, self.lookforward_days + 1)
        estimation_indexes = range(-self.estimation_period - self.lookback_days, - self.lookback_days)
        self.equities_window = pd.DataFrame(index=windows_indexes)
        self.equities_estimation = pd.DataFrame(index=estimation_indexes)
        self.market_window = pd.DataFrame(index=windows_indexes)
        self.market_estimation = pd.DataFrame(index=estimation_indexes)

        dr_data = Calculator.returns(data)
        dr_market = Calculator.returns(market)
        self.dr_equities_window = pd.DataFrame(index=windows_indexes)
        self.dr_equities_estimation = pd.DataFrame(index=estimation_indexes)
        self.dr_market_window = pd.DataFrame(index=windows_indexes)
        self.dr_market_estimation = pd.DataFrame(index=estimation_indexes)

        # 2. Iterate over the list of events and fill the DataFrames
        for i in range(len(self.list)):
            symbol = self.list[i]
            evt_date = self.list.index[i].to_pydatetime()
            col_name = symbol + ' ' + evt_date.strftime('%Y-%m-%d')
            evt_idx = DateUtils.search_closer_date(evt_date, data[symbol].index, exact=True)
            
            # 1.1 Data on the estimation period: self.equities_estimation
            start_idx = evt_idx - self.lookback_days - self.estimation_period # estimation start idx on self.data
            end_idx = evt_idx - self.lookback_days # estimation end idx on self.data
            new_equities_estimation = data[symbol][start_idx:end_idx]
            new_equities_estimation.index = self.equities_estimation.index
            self.equities_estimation[col_name] = new_equities_estimation
            # Daily return of the equities on the estimation period
            new_dr_equities_estimation = dr_data[symbol][start_idx:end_idx]
            new_dr_equities_estimation.index = self.dr_equities_estimation.index
            self.dr_equities_estimation[col_name] = new_dr_equities_estimation

            # 1.4 Market on the estimation period: self.market_estimation
            new_market_estimation = market[self.field][start_idx:end_idx]
            new_market_estimation.index = self.market_estimation.index
            self.market_estimation[col_name] = new_market_estimation
            # Daily return of the market on the estimation period
            new_dr_market_estimation = dr_market[start_idx:end_idx]
            new_dr_market_estimation.index = self.dr_market_estimation.index
            self.dr_market_estimation[col_name] = new_dr_market_estimation

            # 1.3 Equities on the event window: self.equities_window
            start_idx = evt_idx - self.lookback_days # window start idx on self.data
            end_idx = evt_idx + self.lookforward_days + 1 # window end idx on self.data
            new_equities_window = data[symbol][start_idx:end_idx]
            new_equities_window.index = self.equities_window.index
            self.equities_window[col_name] = new_equities_window
            # Daily return of the equities on the event window
            new_dr_equities_window = dr_data[symbol][start_idx:end_idx]
            new_dr_equities_window.index = self.dr_equities_window.index
            self.dr_equities_window[col_name] = new_dr_equities_window

            # 1.4 Market on the event window: self.market_window
            new_market_window = market[self.field][start_idx:end_idx]
            new_market_window.index = self.market_window.index
            self.market_window[col_name] = new_market_window
            # Daily return of the market on the event window
            new_dr_market_window = dr_market[start_idx:end_idx]
            new_dr_market_window.index = self.dr_market_window.index
            self.dr_market_window[col_name] = new_dr_market_window

        # 3. Calculate the linear regression -> expected return
        self.reg_estimation = pd.DataFrame(index=self.dr_market_estimation.columns,
                                        columns=['Intercept', 'Slope', 'Std Error'])
        self.er = pd.DataFrame(index=self.dr_market_window.index,
                                        columns=self.dr_market_window.columns)
        # For each column (event) on the estimation period
        for col in self.dr_market_estimation.columns:
            # 3.1 Calculate the regression
            x = self.dr_market_estimation[col]
            y = self.dr_equities_estimation[col]
            slope, intercept, r_value, p_value, slope_std_error = stats.linregress(x, y)
            self.reg_estimation['Slope'][col] = slope
            self.reg_estimation['Intercept'][col] = intercept
            self.reg_estimation['Std Error'][col] = slope_std_error
            # 3.2 Calculate the expected return of each date using the regression
            self.er[col] = intercept + self.dr_market_window[col] * slope

        # 4. Final results
        self.er.columns.name = 'Expected return'
        self.mean_er = self.er.mean(axis=1)
        self.mean_er.name = 'Mean ER'
        self.std_er = self.er.std(axis=1)
        self.std_er.name = 'Std ER'

        self.ar = self.dr_equities_window - self.er
        self.ar.columns.name = 'Abnormal return'
        self.mean_ar = self.ar.mean(axis=1)
        self.mean_ar.name = 'Mean AR'
        self.std_ar = self.ar.std(axis=1)
        self.std_ar.name = 'Std AR'

        self.car = self.ar.apply(np.cumsum)
        self.car.columns.name = 'Cum Abnormal Return'
        self.mean_car = self.car.mean(axis=1)
        self.mean_car.name = 'Mean CAR'
        self.std_car = self.car.std(axis=1)
        self.mean_car.name = 'Mean CAR'

    def plot(self, which):
        x = self.mean_car.index.values
        if which == 'car':
            y = self.mean_car.values
            yerr = self.std_car.values
            label = self.mean_car.name
        elif which == 'ar':
            y = self.mean_ar.values
            yerr = self.std_ar.values
            label = self.mean_ar.name
        elif which == 'er':
            y = self.mean_er.values
            yerr = self.std_er.values
            label = self.mean_er.name
        errorfill(x, y, yerr, label=label)

if __name__ == '__main__':
    from datetime import datetime
    import matplotlib.pyplot as plt
    from finance.events import EventFinder
    from finance.events import SampleConditions

    evtf = EventFinder()
    evtf.symbols = ['AMD', 'CBG']
    evtf.start_date = datetime(2008, 1, 1)
    evtf.end_date = datetime(2009, 12, 31)
    evtf.condition = SampleConditions.went_below(3)
    evtf.search()

    mevt = MultipleEvents()
    mevt.list = evtf.list
    mevt.market = 'SPY'
    mevt.lookback_days = 20
    mevt.lookforward_days = 20
    mevt.estimation_period = 200
    mevt.run()
    print(mevt.mean_car)

    #mevt.plot('car')
    #plt.legend()
    #plt.show()
