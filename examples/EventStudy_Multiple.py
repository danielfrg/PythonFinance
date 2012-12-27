from datetime import datetime
from finance.evtstudy import EventFinder, MultipleEvents

evtf = EventFinder('./data')
evtf.symbols = ['AMD', 'CBG']
evtf.start_date = datetime(2008, 1, 1)
evtf.end_date = datetime(2009, 12, 31)
evtf.function = evtf.went_below(3)
evtf.search()

mevt = MultipleEvents('./data')
mevt.matrix = evtf.matrix
mevt.market = 'SPY'
mevt.lookback_days = 20
mevt.lookforward_days = 20
mevt.estimation_period = 200
mevt.run()

print(mevt.mean_abnormal_return)

import matplotlib
matplotlib.use('Qt4Agg') # Probably most people dont need this line
import matplotlib.pyplot as plt
mevt.mean_cumulative_abnormal_return.plot()
plt.show()