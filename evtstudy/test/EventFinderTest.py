import unittest
import numpy as np
import pandas as pd
import numpy.testing as np_test
import pandas.util.testing as pd_test
from datetime import datetime
from finance.utils import DataAccess
from finance.evtstudy import EventFinder

class EventFinderTest(unittest.TestCase):
    def setUp1(self):
        DataAccess('./data').empty_cache()

    def suite(self):
        suite = unittest.TestSuite()
        suite.addTest(EventFinderTest('test_oneEventPerEquity'))
        suite.addTest(EventFinderTest('test_reduceMatrix'))
        # suite.addTest(EventFinderTest('test_3'))
        return suite

    def test_oneEventPerEquity(self):
        '''
        Equities: AMD
        Function: went_below(3)
        Period: 2008-1-1 -> 2009-12-31

        Tests: oneEventPerEquity=True and oneEventPerEquity=False
        '''
        self.setUp1()

        evtf = EventFinder('./data')
        evtf.symbols = ['AMD']
        evtf.start_date = datetime(2008, 1, 1)
        evtf.end_date = datetime(2009, 12, 31)
        evtf.function = evtf.went_below(3)
        evtf.search(oneEventPerEquity=True)
        # Test: number of events found = 1
        self.assertEqual(evtf.num_events, 1)
        # Test: date of the event is 2008-10-27
        date1 = evtf.matrix['AMD'][evtf.matrix['AMD'] == 1].index[0].to_pydatetime()
        self.assertEqual(date1, datetime(2008,10,27))

        # Test: oneEventPerEquity=False
        evtf.search(oneEventPerEquity=False)
        # Test: number of events found = 2
        self.assertEqual(evtf.num_events, 2)
        # Test: date of the events
        date1 = evtf.matrix['AMD'][evtf.matrix['AMD'] == 1].index[0].to_pydatetime()
        date2 = evtf.matrix['AMD'][evtf.matrix['AMD'] == 1].index[1].to_pydatetime()
        self.assertEqual(date1, datetime(2008,10,27))
        self.assertEqual(date2, datetime(2008,11,11))

    def test_reduceMatrix(self):
        '''
        Equities: AMD, CGB
        Function: went_below(3)
        Period: 2008-1-1 -> 2009-12-31

        Tests: reduceMatrix=True and reduceMatrix=False
        '''
        self.setUp1()

        evtf = EventFinder('./data')
        evtf.symbols = ['AMD' ,'CBG']
        evtf.start_date = datetime(2008, 1, 1)
        evtf.end_date = datetime(2009, 12, 31)
        evtf.function = evtf.went_below(3)

        # Test: reduceMatrix=False
        evtf.search(reduceMatrix=False)
        self.assertEqual(len(evtf.matrix), 505)
        self.assertEqual(evtf.num_events, 2)
        # Test: date of the events
        date1 = evtf.matrix['AMD'][evtf.matrix['AMD'] == 1].index[0].to_pydatetime()
        self.assertEqual(date1, datetime(2008,10,27))
        date2 = evtf.matrix['CBG'][evtf.matrix['CBG'] == 1].index[0].to_pydatetime()
        self.assertEqual(date2, datetime(2009,2,27))

        # Test: reduceMatrix=True
        evtf.search(reduceMatrix=True)
        self.assertEqual(len(evtf.matrix), 2)
        self.assertEqual(evtf.num_events, 2)
        # Test: date of the events
        date1 = evtf.matrix['AMD'][evtf.matrix['AMD'] == 1].index[0].to_pydatetime()
        self.assertEqual(date1, datetime(2008,10,27))
        date2 = evtf.matrix['CBG'][evtf.matrix['CBG'] == 1].index[0].to_pydatetime()
        self.assertEqual(date2, datetime(2009,2,27))

if __name__ == '__main__':
    suite = EventFinderTest().suite()
    unittest.TextTestRunner(verbosity=2).run(suite)

    #DataAccess('./data').empty_dirs(delete=True)