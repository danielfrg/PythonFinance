from datetime import datetime
from finance.data import DataAccess

da = DataAccess('./data')
symbols = ["AAPL", "GLD", "GOOG", "SPY", "XOM"]
start_date = datetime(2008, 1, 1)
end_date = datetime(2009, 12, 31)
fields = "Close"

close = da.get_data(symbols, start_date, end_date, fields)
print(close)
