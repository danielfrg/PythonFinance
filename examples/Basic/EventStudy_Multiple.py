from datetime import datetime
import matplotlib.pyplot as plt
from finance.events import EventFinder
from finance.events import MultipleEvents
from finance.events import SampleConditions

# from finance.utils import DataAccess
# DataAccess.path = 'data'

evtf = EventFinder()
evtf.symbols = ['AMD', 'CBG']
evtf.start_date = datetime(2008, 1, 1)
evtf.end_date = datetime(2009, 12, 31)
evtf.condition = SampleConditions.went_below(3)
evtf.search()
print(evtf.list)

mevt = MultipleEvents()
mevt.list = evtf.list
mevt.market = 'SPY'
mevt.lookback_days = 20
mevt.lookforward_days = 20
mevt.estimation_period = 200
mevt.run()

print(mevt.mean_ar)

mevt.plot('car')
plt.show()
