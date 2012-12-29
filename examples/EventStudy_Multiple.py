from datetime import datetime
import matplotlib.pyplot as plt
from finance.utils import DataAccess
from finance.events import EventFinder, MultipleEvents

DataAccess.path = 'data'
da = DataAccess()

evtf = EventFinder()
evtf.symbols = ['AMD', 'CBG']
evtf.start_date = datetime(2008, 1, 1)
evtf.end_date = datetime(2009, 12, 31)
evtf.function = evtf.went_below(3)
evtf.search()

mevt = MultipleEvents()
mevt.list = evtf.list
mevt.market = 'SPY'
mevt.lookback_days = 20
mevt.lookforward_days = 20
mevt.estimation_period = 200
mevt.run()

print(mevt.mean_abnormal_return)

mevt.mean_cumulative_abnormal_return.plot()
plt.show()

mevt.plot('car')
plt.show()
