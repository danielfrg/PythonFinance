from datetime import datetime
from finance.evtstudy import PastEvent

pevt = PastEvent('./data')
pevt.symbol = 'AAPL'
pevt.market = "^gspc"
pevt.lookback_days = 10
pevt.lookforward_days = 10
pevt.estimation_period = 252
pevt.date = datetime(2009, 1, 5)
pevt.run()

print(pevt.er)