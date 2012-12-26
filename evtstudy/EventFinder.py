import numpy as np
import pandas as pd

from datetime import datetime
from finance.utils import DateUtils
from finance.utils import DataAccess

class EventFinder(object):
    def __init__(self, path='./data/'):
        self.path = path
        self.data_access = DataAccess(path)

        self.symbols = []
        self.start_date = None
        self.end_date = None
        self.field = 'Adj Close'

        self.function = None
        self.funcion_name = None
        self.matrix = None
        self.num_events = 0

        self.reduceMatrix = True
        self.oneEventPerEquity = True

    def generate_filename(self):
        return '%s%s%s%s%s%s%s' % (''.join(self.symbols), self.start_date.strftime('%m-%d-%Y'),
                self.end_date.strftime('%m-%d-%Y'), self.field, self.funcion_name,
                str(self.reduceMatrix), str(self.oneEventPerEquity))

    def search(self, reduceMatrix=True, oneEventPerEquity=True, useCache=True, save=True):
        self.reduceMatrix = reduceMatrix
        self.oneEventPerEquity = oneEventPerEquity

        if useCache:
            self.matrix = self.data_access.load(self.generate_filename(), '.evt_matrix')
            if self.matrix is not None:
                self.num_events = self.matrix.count().sum(axis=0)
                return

        # 0. Get the dates, and Download/Import the data
        nyse_dates = DateUtils.nyse_dates(start=self.start_date, end=self.end_date, list=True)
        data = self.data_access.get_data(self.symbols, nyse_dates[0], nyse_dates[-1], self.field)
        # Special case
        if len(data.columns) == 1:
            data.columns = self.symbols
        # 1. Create and fill the matrix of events
        data = data[self.start_date:self.end_date]
        self.matrix = pd.DataFrame(index=data.index, columns=self.symbols)

        for symbol in self.symbols:
            i = 0
            for item in data[symbol][1:]:
                e = self.function(i, item, data[symbol][1:])
                if e:
                    self.matrix[symbol][i+1] = 1
                    if oneEventPerEquity == True:
                        break
                i = i + 1

        if reduceMatrix:
            # Sum each row and if is greater than 0 there is an event
            self.matrix = self.matrix[self.matrix.fillna(value=0).sum(axis=1) > 0]


        # 2. Calculate other results and save if requested
        self.num_events = self.matrix.count().sum(axis=0)
        if save:
            self.data_access.save(self.matrix, self.generate_filename(), '.evt_matrix')

    def decrease(self, decrease):
        self.funcion_name = 'decrease_%d' % decrease
        return lambda i, item, data: (data[i-1] - item > decrease)

    def increase(self, increase):
        self.funcion_name = 'increase_%d' % increase
        return lambda i, item, data: (item - data[i-1] > increase)

    def went_below(self, below):
        self.funcion_name = 'below_%d' % below
        return lambda i, item, data: (data[i-1] >= below and item < below)

    def went_above(self, above):
        self.funcion_name = 'above_%d' % above
        return lambda i, item, data: (data[i-1] <= above and item > above)

if __name__ == '__main__':
    
    evtf = EventFinder('./data')
    evtf.symbols = ['AMD', 'CBG']
    evtf.start_date = datetime(2008, 1, 1)
    evtf.end_date = datetime(2010, 12, 31)
    evtf.function = evtf.went_below(3)
    evtf.search(reduceMatrix=True)

    # print(evtf.num_events)
    # print(evtf.matrix)
