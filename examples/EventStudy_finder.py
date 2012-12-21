from datetime import datetime
from finance.evtstudy import EventFinder

evt_finder = EventFinder('./data')
evt_finder.symbols = ['AAPL', 'GOOG', 'XOM']
evt_finder.search()
