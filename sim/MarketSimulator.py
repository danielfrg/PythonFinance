import pandas as pd
from finance.utils import DataAccess
from datetime import datetime
from datetime import date

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

        self.trades = None
        self.prices = None
        self.own = None
        self.cash = None
        self.equities = None
        self.portfolio = None

    def load_trades(self, file_path):
        '''
        Reads the csv file and parse the data
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

    def simulate(self, trades=None, ordersIsDataFrame=False):
        '''
        Simulates the trades, fills the DataFrames: cash, equities_value, porfolio
        '''
        # 0. Init the required data
        # 0.1 if trades is not None load them
        if trades is not None:
            if ordersIsDataFrame:
                self.set_trades(trades)
            else:
                # If there is no DataFrame then is a file to be loaded
                self.load_trades(trades)
        # 0.2 Load/Download required data
        symbols = list(set(self.trades['symbol']))
        start_date = self.trades.index[0].to_pydatetime()  # Convert from TimeStamp to datetime
        end_date = self.trades.index[-1].to_pydatetime()
        self.prices = self.da.get_data(symbols, start_date, end_date, "Adj Close")
        # 0.3 Init other DataFrames, dictionaries
        self.cash = pd.DataFrame(index=self.prices.index, columns=['Cash'])
        self.own = pd.DataFrame(index=self.prices.index, columns=self.prices.columns)
        current_stocks = dict([(symbol, 0) for symbol in list(set(self.trades['symbol']))])
        # 0.3 Set the current cash to the initial cash before star the simulation
        self.current_cash = self.initial_cash

        # 1. Fill the DataFrames
        for idx, row in self.trades.iterrows():
            # For each order
            # Note: idx is Timestamp, row is Series
            # Note 2: If there are various trades on the same day overwrites the previous value.

            # 1.0 Get info of the row
            symbol = row['symbol']
            action = row['action'].lower()[0:1]
            num_of_shares = row['num_of_shares']

            # 1.1 Fill the cash DataFrame
            # Get the change of cash on the order
            cash_change = self.prices[symbol][idx] * num_of_shares
            if action == 'b':
                self.current_cash = self.current_cash - cash_change
            elif action == 's':
                self.current_cash = self.current_cash + cash_change
            # Modify self.cash DataFrame
            self.cash.ix[idx] = self.current_cash

            # 1.2 Fill the own DataFrame - num of stocks on each date
            if action == 'b':
                current_stocks[symbol] = current_stocks[symbol] + num_of_shares
            elif action == 's':
                current_stocks[symbol] = current_stocks[symbol] - num_of_shares
            # Modify self.own DataFrame
            self.own.ix[idx][symbol] = current_stocks[symbol]

        # Fill forward missing values
        self.cash = self.cash.fillna(method='ffill')
        self.own = self.own.fillna(method='ffill')
        # After forward-fill fill with zeros because initial values are still NaN
        self.own = self.own.fillna(0)

        # 2. Get the value of the equitues
        self.equities = self.own * self.prices
        self.equities = self.equities.sum(1)

        # 3. Get the value of the porfolio = cash + equities_value
        self.portfolio = self.cash + self.equities
        self.portfolio.columns = ['Portfolio']

if __name__ == "__main__":
    sim = MarketSimulator('./test/data2')
    sim.initial_cash = 1000000
    sim.load_trades("../examples/MarketSimulator_orders.csv")
    sim.simulate()
    print(sim.portfolio.tail())




