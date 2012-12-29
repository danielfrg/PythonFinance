import numpy as np
import pandas as pd
from datetime import datetime
from finance.utils import DataAccess
from finance.utils import DateUtils

class MarketSimulator(object):
    '''
    Market Simulator

    Needs a list of trades to simulate, options are:
        1. Provide a custom pandas.DataFrame(index=DatetimeIndex):
                        symbol  action    num_of_shares
            2011-01-10   AAPL    Buy           1500
            2011-01-13   AAPL    Sell          1500
            2011-01-13   IBM     Buy           4000
            2011-01-26   GOOG    Buy           1000
        2. Load the trades from a csv file:
            year,month,day,symbol,action,num_of_shares
            2011,1,10,AAPL,Buy,1500
            2011,1,13,AAPL,Sell,1500
            2011,1,13,IBM,Buy,4000
            2011,1,26,GOOG,Buy,1000
        3. Create trades from an event list:
            TODO: example
    '''
    def __init__(self):
        self.da = DataAccess()

        self.initial_cash = 0
        self.field = "Adj Close"

        self.trades = None
        self.prices = None
        self.num_of_shares = None
        self.cash = None
        self.equities = None
        self.portfolio = None

    def load_trades(self, file_path):
        '''
        Load trades from a csv file

        csv file example:
        year,month,day,symbol,action,num_of_shares
        2011,1,10,AAPL,Buy,1500
        2011,1,13,AAPL,Sell,1500
        2011,1,13,IBM,Buy,4000
        2011,1,26,GOOG,Buy,1000

        Parameters
        ----------
            file_path: str, path to the csv containing the orders

        '''
        # 1. Read the .csv file
        self.trades = pd.read_csv(file_path)

        # 2. Set the indexes as the value of a the columns (year, month, day)
        dates = list()
        for idx, row in self.trades.iterrows():
            date = datetime(row['year'], row['month'], row['day'])
            dates.append(date)
        dates = pd.Series(dates)
        self.trades = self.trades.set_index(dates)

        # 3. Delete unnescessary columns
        self.trades = self.trades[['symbol', 'action', 'num_of_shares']]
        
        # 4. Sort the DataFrame by the index (dates)
        self.trades = self.trades.sort()

    def create_trades_from_event(self, eventList, 
                                eventDayAction='Buy', eventDayShares=100,
                                actionAfter='Sell', daysAfter=5, sharesAfter=100,
                                actionBefore=None, daysBefore=5, sharesBefore=100):
        '''
        Creates trades using an event list; usually from the EventFinder.
        Also creates aditional order after and before of the event as defined by the user

        Parameters
        ----------
            eventList: pandas.Series
        '''
        self.trades = pd.DataFrame(index=eventList.index, columns=['symbol', 'action', 'num_of_shares'])
        self.trades['symbol'] = eventList
        self.trades['action'] = eventDayAction
        self.trades['num_of_shares'] = eventDayShares

        # TODO: Actions BEFORE

        if actionAfter is not None:
            dicts = []
            for idx, row in self.trades.iterrows():
                after_date = DateUtils.nyse_add(idx.to_pydatetime(), daysAfter)
                after = pd.DataFrame([  {'symbol': row['symbol'], 
                                        'action': actionAfter, 
                                        'num_of_shares': sharesAfter}],
                                    index=[after_date], columns=self.trades.columns)
                self.trades = self.trades.append(after)

        self.trades = self.trades.sort()
    

    def simulate(self):
        '''
        Simulates the trades

        Parameters
        ----------
            trades: str(filepath) or pandas.DataFrame, if str loads the orders from a csv file

        Returns
        -------
            Nothing: Fills the DataFrames: cash, equities, porfolio
        '''
        # 0.1 Load/Download required data
        symbols = list(set(self.trades['symbol']))
        start_date = self.trades.index[0].to_pydatetime()  # Convert from TimeStamp to datetime
        end_date = self.trades.index[-1].to_pydatetime()  # Convert from TimeStamp to datetime
        self.prices = self.da.get_data(symbols, start_date, end_date, self.field)
        # 0.2 Init DataFrames
        self.cash = pd.DataFrame(index=self.prices.index, columns=['Cash'], dtype=np.float64)
        self.num_of_shares = pd.DataFrame(index=self.prices.index, columns=self.prices.columns, dtype=np.float64)

        # 1. Fill the DataFrames
        current_cash = self.initial_cash
        current_shares = dict([(symbol, 0) for symbol in symbols])
        for idx, row in self.trades.iterrows():
            # 1.2.0 Get info of the row
            symbol = row['symbol']
            action = row['action'].lower()[0:1]
            num_of_shares = row['num_of_shares']

            # 1.2.1 Fill the self.cash DataFrame - ammount of cash on each date
            # NOTE: but stocks spends cash, sell stocks wins cash
            cash_change = self.prices[symbol][idx] * num_of_shares
            if action == 'b':
                current_cash = current_cash - cash_change
            elif action == 's':
                current_cash = current_cash + cash_change
            # Modify self.cash DataFrame
            self.cash.ix[idx] = current_cash

            # 1.2.3 Fill the self.num_of_shares DataFrame - num of each stocks on each date
            if action == 'b':
                current_shares[symbol] = current_shares[symbol] + num_of_shares
            elif action == 's':
                current_shares[symbol] = current_shares[symbol] - num_of_shares
            # Modify self.num_of_shares DataFrame
            self.num_of_shares.ix[idx][symbol] = current_shares[symbol]

        # Fill forward missing values
        self.cash = self.cash.fillna(method='ffill')
        self.prices = self.prices.fillna(method='ffill').fillna(method='bfill')
        self.num_of_shares = self.num_of_shares.fillna(method='ffill').fillna(0)

        # 2. Get the value of the equitues
        self.equities = self.num_of_shares * self.prices
        self.equities = self.equities.sum(axis=1)
        self.equities.columns = ['Equities']

        # 3. Get the value of the porfolio = cash + equities_value
        self.portfolio = self.cash + self.equities
        self.portfolio.columns = ['Portfolio']

if __name__ == "__main__":
    # from finance.evtstudy import EventFinder
    # evtf = EventFinder('./data')
    # evtf.symbols = ['AMD', 'CBG', 'AAPL']
    # evtf.start_date = datetime(2008, 1, 1)
    # evtf.end_date = datetime(2010, 12, 31)
    # evtf.function = evtf.went_below(5)
    # evtf.search(oneEventPerEquity=False)

    # print(evtf.list)

    sim = MarketSimulator('./data')
    sim.field = "Adj Close"
    sim.initial_cash = 1
    # sim.create_trades_from_event(evtf.list)
    sim.load_trades("./test/orders.csv")
    print(sim.trades)
    sim.simulate()

    from finance.utils import BasicUtils
    print(BasicUtils.total_return(sim.portfolio))
    print(BasicUtils.total_return(sim.portfolio.values))

    import matplotlib
    matplotlib.use('Qt4Agg')

    import matplotlib.pyplot as plt
    sim.portfolio.plot()
    plt.show()





