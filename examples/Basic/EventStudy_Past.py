from datetime import datetime
import matplotlib.pyplot as plt
from finance.events import PastEvent

# from finance.utils import DataAccess
# DataAccess.path = 'data'

evt = PastEvent()
evt.symbol = 'AAPL'
evt.market = "^gspc"
evt.lookback_days = 10
evt.lookforward_days = 10
evt.estimation_period = 252
evt.date = datetime(2009, 1, 5)
evt.run()

#print(evt.expected_return)
#print(evt.abnormal_return)
print(evt.car)
#print(evt.t_test)

evt.ar.plot()
plt.show()