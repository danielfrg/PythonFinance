import os
from datetime import datetime
from finance.utils import DataAccess

# os.putenv("FINANCEPATH", 'data')
os.environ["FINANCEPATH"] = './data2'
da2 = DataAccess()

DataAccess.path = 'data'
da = DataAccess()

symbols = ["AAPL", "GLD", "GOOG", "SPY", "XOM"]
start_date = datetime(2008, 1, 1)
end_date = datetime(2009, 12, 31)
fields = "Close"
close = da.get_data(symbols, start_date, end_date, fields)
print(close)

# da.empty_dirs()
da2.empty_dirs()