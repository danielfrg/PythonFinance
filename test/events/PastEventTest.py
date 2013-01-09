import unittest
import numpy as np
import pandas as pd
from datetime import datetime

from finance.test import FinanceTest
from finance.events import PastEvent

class PastEventTest(FinanceTest):

    def suite(self):
        suite = unittest.TestSuite()
        suite.addTest(PastEventTest('test_window'))
        return suite

    def test_window(self):
        '''
        Tests
        -----
            1. Expected returns
            2. Abnormal returns
            3. Cumulative abnormal returns
            4. t-test
        '''
        self.setUpDataAccess()

        evt = PastEvent()
        evt.symbol = 'AAPL'
        evt.market = "^gspc"
        evt.lookback_days = 10
        evt.lookforward_days = 10
        evt.estimation_period = 252
        evt.date = datetime(2009, 1, 5)
        evt.run()

        tests = ['docs/PastEvent_window_1.csv']
        
        for test_file in tests:
            # Set up
            solution = pd.read_csv(test_file)
            solution.index = evt.er.index
            # Test 1
            self.assertEqual(evt.er, solution['Expected return'], 3)
            # Test 2
            self.assertEqual(evt.ar, solution['Abnormal return'], 3)
            # Test 3
            self.assertEqual(evt.car, solution['Cum abnormal return'], 2)
            # Test 4
            self.assertEqual(evt.t_test, solution['t-test'], 2)

if __name__ == '__main__':
    suite = PastEventTest().suite()
    unittest.TextTestRunner(verbosity=2).run(suite)

    # FinanceTest.delete_data()