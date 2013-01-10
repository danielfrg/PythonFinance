from datetime import datetime
from finance.events import SampleConditions
from finance.events import EventFinder

# from finance.utils import DataAccess
# DataAccess.path = 'data'

evtf = EventFinder()
evtf.symbols = ['AMD', 'CBG', 'AAPL']
evtf.start_date = datetime(2008, 1, 1)
evtf.end_date = datetime(2010, 12, 31)
evtf.condition = SampleConditions.went_below(10)
evtf.search(useCache=False)

print(evtf.num_events)
print(evtf.list)
