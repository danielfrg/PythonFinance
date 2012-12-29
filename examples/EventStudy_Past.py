from datetime import datetime
import matplotlib.pyplot as plt
from finance.utils import DataAccess
from finance.events import PastEvent

DataAccess.path = 'data'
da = DataAccess()

pevt = PastEvent()
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


pevt.cumulative_abnormal_return.plot()
plt.show()