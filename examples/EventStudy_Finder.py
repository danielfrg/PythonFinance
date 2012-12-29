from datetime import datetime
from finance.utils import DataAccess
from finance.events import EventFinder

DataAccess.path = 'data'
da = DataAccess()

evtf = EventFinder()
evtf.symbols = ['AMD', 'CBG', 'AAPL']
evtf.start_date = datetime(2008, 1, 1)
evtf.end_date = datetime(2010, 12, 31)
evtf.function = evtf.went_below(3)
evtf.search()

# print(evtf.num_events)
print(evtf.list)
