from datetime import datetime
import matplotlib.pyplot as plt
from finance.events import SampleEvents
from finance.events import EventFinder, MultipleEvents

# from finance.utils import DataAccess
# DataAccess.path = 'data'

evtf = EventFinder()
evtf.symbols = ['AMD', 'CBG']
evtf.start_date = datetime(2008, 1, 1)
evtf.end_date = datetime(2009, 12, 31)
evtf.event = SampleEvents.went_below(3)
evtf.search()

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
