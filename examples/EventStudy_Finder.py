from datetime import datetime
from finance.events import EventFinder
    
evtf = EventFinder('./data')
evtf.symbols = ['AMD', 'CBG', 'AAPL']
evtf.start_date = datetime(2008, 1, 1)
evtf.end_date = datetime(2010, 12, 31)
evtf.function = evtf.went_below(3)
evtf.search()

# print(evtf.num_events)
print(evtf.list)
