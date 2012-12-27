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

#print(pevt.expected_return)
#print(pevt.abnormal_return)
print(pevt.cumulative_abnormal_return)
#print(pevt.t_test)

import matplotlib
matplotlib.use('Qt4Agg') # Probably most people dont need this line
import matplotlib.pyplot as plt
pevt.expected_return.plot()
plt.show()