import os
from datetime import datetime
from finance.utils import DataAccess

# Option 1: Set the Enviroment Variable FINANCEPATH
os.environ["FINANCEPATH"] = './data'
da = DataAccess()
symbols = ["GOOG", "SPY", "XOM"]
start_date = datetime(2015, 1, 1)
end_date = datetime(2017, 12, 31)
fields = 'close'
close = da.get_data(symbols, start_date, end_date, fields)
print(close)

# Option 2: Manualy set the PATH, overwrites option 1

DataAccess.path = 'data2'
da = DataAccess()

symbols = ["AAPL", "GLD"]
start_date = datetime(2015, 1, 1)
end_date = datetime(2017, 12, 31)
fields = 'close'
close = da.get_data(symbols, start_date, end_date, fields)
print(close)

