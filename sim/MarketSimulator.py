import pandas as pd
from finance.data import DataAccess
from datetime import datetime
from datetime import date

class MarketSimulator(object):
    '''
    Market Simulator.
    Receives:
        1. Initial cash
        2. List of trades (automaticly search and downloads missing information)
    After simulation:
        pandas.DataFrame with the value of the portfolio

    '''
    def __init__(self, path='./data'):
        self.da = DataAccess(path)

        self.initial_cash = 0
        self.current_cash = 0

        self.trades = None
        self.prices = None
        self.own = None
        self.cash = None
        self.equities_value = None
        self.porfolio = None

    def set_initial_cash(self, cash):
        self.initial_cash = cash
        self.current_cash = cash

    def get_portfolio(self):
        return self.porfolio

    def load_trades(self, file_path):
        '''
        Reads the csv file and call self.set_trades()
        '''
        self.set_trades(pd.read_csv(file_path))

    def set_trades(self, trades):
        '''
        Load the trades, loads the necesary data, initialize the DataFrames needed
        '''
        # 1. Parse the trades file
        # 1.1 Set the indexes as the value of a the columns (year, month, day)
        dates = list()
        for idx, row in trades.iterrows():
            date = datetime(row['year'], row['month'], row['day'])
            dates.append(date)
        dates = pd.Series(dates)
        trades = trades.set_index(dates)
        # 1.2 Delete unnescessary columns, also make the data var global to the class
        self.trades = trades[['symbol', 'action', 'num_of_shares']]
        # 1.3 Sort the DataFrame by the index (dates)
        self.trades = self.trades.sort()

        # 2. Load the prices data
        symbols = list(set(self.trades['symbol']))
        start_date = self.trades.index[0].to_pydatetime()  # Convert from TimeStamp to datetime
        end_date = self.trades.index[len(dates)-1].to_pydatetime()
        self.prices = self.da.get_data(symbols, start_date, end_date, "Adj Close")


    def simulate(self):
        '''
        Simulates the trades, fills the DataFrames: cash, equities_value, porfolio
        '''
        # 0. Init other DataFrames, dictionaries
        self.cash = pd.DataFrame(index=self.prices.index, columns=['Cash'])
        self.own = pd.DataFrame(index=self.prices.index, columns=self.prices.columns)
        current_stocks = dict([(symbol, 0) for symbol in list(set(self.trades['symbol']))])

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
            # Get the change of number of shares
            self.own.ix[idx][symbol] = num_of_shares
            if action == 'b':
                current_stocks[symbol] = current_stocks[symbol] + num_of_shares
            elif action == 's':
                current_stocks[symbol] = current_stocks[symbol] - num_of_shares
            # Modify self.own DataFrame
            self.own.ix[idx][symbol] = current_stocks[symbol]

        # Fill forward missing values
        self.cash = self.cash.fillna(method='ffill')
        self.own = self.own.fillna(method='ffill')
        # After ffill fill with zeros because initial values are still NaN
        self.own = self.own.fillna(0)

        # 2. Get the value of the equitues
        self.equities_value = self.own * self.prices
        self.equities_value = self.equities_value.sum(1)

        # 3. Get the value of the porfolio = cash + equities_value
        self.porfolio = self.cash + self.equities_value
        self.porfolio.columns = ['Portfolio']

if __name__ == "__main__":
    sim = MarketSimulator('../examples/data')
    sim.set_initial_cash(1000000)
    sim.load_trades("../examples/orders.csv")
    sim.simulate()




