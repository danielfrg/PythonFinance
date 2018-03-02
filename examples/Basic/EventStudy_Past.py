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

#print("Expected Return: {0}".format(evt.er))
#print("Abnormal Return: {0}".format(evt.ar))
print(evt.car)
#print("T Test: {0}".format(evt.t_test))

evt.ar.plot()
plt.show()