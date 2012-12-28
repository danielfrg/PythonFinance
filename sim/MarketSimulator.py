import numpy as np
import pandas as pd
from datetime import datetime
from finance.utils import DataAccess
from finance.utils import DateUtils

class MarketSimulator(object):
    '''
    Market Simulator.
    Receives:
        1. Initial cash
        2. List of trades (automaticly search and downloads missing information)
    After simulation:
        portfolio is a pandas.DataFrame with the values of the portfolio on each date

    '''
    def __init__(self, path='./data'):
        self.da = DataAccess(path)

        self.initial_cash = 0
        self.current_cash = 0
        self.field = "Adj Close"

        self.trades = None
        self.prices = None
        self.own = None
        self.cash = None
        self.equities = None
        self.portfolio = None

    def load_trades(self, file_path):
        '''
        Reads the csv file and parse the data

        Parameters
        ----------
            file_path: str, path to the csv containing the orders

        Returns
        -------
            Nothing: the trades are ready to simulate
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

    def create_trades_from_event(self, eventList, eventDayAction='Buy', eventDayShares=100,
                                actionAfter='Sell', daysAfter=5, sharesAfter=100,
                                actionBefore='But', daysBefore=5, sharesBefore=100):
        '''
        Creates trades using an event list

        Parameters
        ----------
            eventList: pandas.Series - usually the list created by the EventFinder
        '''
        self.trades = pd.DataFrame(index=eventList.index, columns=['symbol', 'action', 'num_of_shares'])
        self.trades['symbol'] = eventList
        self.trades['action'] = eventDayAction
        self.trades['num_of_shares'] = eventDayShares

        # TODO: Actions BEFORE

        if actionAfter is not None:
            dicts = []
            for idx, row in self.trades.iterrows():
                after_date = DateUtils.add(idx.to_pydatetime(), daysAfter)
                after = pd.DataFrame([  {'symbol': row['symbol'], 
                                        'action': actionAfter, 
                                        'num_of_shares': sharesAfter}],
                                    index=[after_date], columns=self.trades.columns)
                self.trades = self.trades.append(after)

        self.trades = self.trades.sort()
    

    def simulate(self, trades=None):
        '''
        Simulates the trades

        Parameters
        ----------
            trades: str(filepath) or pandas.DataFrame, if str loads the orders from a csv file

        Returns
        -------
            None: Fills the DataFrames: cash, equities_value, porfolio
        '''
        # 0. Init the required data
        # 0.1 if trades is not None load them
        if trades is not None:
            if type(trades) is pd.DataFrame:
                self.trades = trades
            else:
                # If orders no DataFrame then is a file to be loaded
                self.load_trades(trades)
        # 0.2 Load/Download required data
        symbols = list(set(self.trades['symbol']))
        start_date = self.trades.index[0].to_pydatetime()  # Convert from TimeStamp to datetime
        end_date = self.trades.index[-1].to_pydatetime()
        self.prices = self.da.get_data(symbols, start_date, end_date, self.field)
        # 0.3 Init other DataFrames
        self.cash = pd.DataFrame(index=self.prices.index, columns=['Cash'], dtype=np.float64)
        self.own = pd.DataFrame(index=self.prices.index, columns=self.prices.columns, dtype=np.float64)

        # 1. Fill the DataFrames
        # 1.1 current_stocks e.g.: [('AAPL', 0), ('GOOG', 0)]
        current_stocks = dict([(symbol, 0) for symbol in list(set(self.trades['symbol']))])
        # 1.1 Set the current cash to the initial cash before star the simulation
        self.current_cash = self.initial_cash
        for idx, row in self.trades.iterrows():
            # For each order
            # Note: If there are various trades on the same day overwrites the previous value
            # which is the correct behavior

            # 1.0 Get info of the row
            symbol = row['symbol']
            action = row['action'].lower()[0:1]
            num_of_shares = row['num_of_shares']

            # 1.1 Fill the self.cash DataFrame - ammount of cash on each date
            # change of cash on the order
            cash_change = self.prices[symbol][idx] * num_of_shares
            if action == 'b':
                self.current_cash = self.current_cash - cash_change
            elif action == 's':
                self.current_cash = self.current_cash + cash_change
            # Modify self.cash DataFrame
            self.cash.ix[idx] = self.current_cash

            # 1.2 Fill the self.own DataFrame - num of each stocks on each date
            if action == 'b':
                current_stocks[symbol] = current_stocks[symbol] + num_of_shares
            elif action == 's':
                current_stocks[symbol] = current_stocks[symbol] - num_of_shares
            # Modify self.own DataFrame
            self.own.ix[idx][symbol] = current_stocks[symbol]

        # Fill forward missing values
        self.cash = self.cash.fillna(method='ffill')
        self.prices = self.prices.fillna(method='ffill').fillna(method='bfill')
        self.own = self.own.fillna(method='ffill').fillna(0)

        # 2. Get the value of the equitues
        self.equities = self.own * self.prices
        self.equities = self.equities.sum(axis=1)
        self.equities.columns = ['Equities']

        # 3. Get the value of the porfolio = cash + equities_value
        self.portfolio = self.cash + self.equities
        self.portfolio.columns = ['Portfolio']

if __name__ == "__main__":
    from finance.evtstudy import EventFinder
    evtf = EventFinder('./data')
    evtf.symbols = ['AMD', 'CBG', 'AAPL']
    evtf.start_date = datetime(2008, 1, 1)
    evtf.end_date = datetime(2010, 12, 31)
    evtf.function = evtf.went_below(5)
    evtf.search(oneEventPerEquity=False)

    # print(evtf.list)

    sim = MarketSimulator('./data')
    sim.field = "Adj Close"
    sim.initial_cash = 1
    sim.create_trades_from_event(evtf.list)
    # print(sim.trades)
    # sim.load_trades("./test/orders.csv")
    sim.simulate()

    from finance.utils import BasicUtils
    print(BasicUtils.total_return(sim.portfolio))
    print(BasicUtils.total_return(sim.portfolio.values))

    import matplotlib
    matplotlib.use('Qt4Agg')

    import matplotlib.pyplot as plt
    #sim.portfolio.plot()
    #plt.show()





