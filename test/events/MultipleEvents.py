import unittest
import os, inspect
import numpy as np
import pandas as pd
from datetime import datetime

from finance.test import FinanceTest
from finance.events import EventFinder
from finance.events import SampleConditions
from finance.events import MultipleEvents

class MultipleEventsTest(FinanceTest):

    def suite(self):
        suite = unittest.TestSuite()
        suite.addTest(MultipleEventsTest('test_window'))
        return suite

    def test_window(self):
        '''
        Two events on two different equities

        Tests
        -----
            1. Expected returns
            2. Abnormal returns
            3. Cumulative abnormal returns
            4. Mean of ER, AR, CAR
        '''
        # Set Up
        self.setUpDataAccess()

        evt_fin = EventFinder()
        evt_fin.symbols = ['AMD', 'CBG']
        evt_fin.start_date = datetime(2008, 1, 1)
        evt_fin.end_date = datetime(2009, 12, 31)
        evt_fin.condition = SampleConditions.went_below(3)
        evt_fin.search()
        
        mul_evt = MultipleEvents()
        mul_evt.list = evt_fin.list
        mul_evt.market = 'SPY'
        mul_evt.lookback_days = 20
        mul_evt.lookforward_days = 20
        mul_evt.estimation_period = 200
        mul_evt.run()

        self_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        tests = ['MultipleEvents_window_1.csv']
        tests = [os.path.join(self_dir, 'docs', test) for test in tests]
        
        for test_file in tests:
            # Set up
            solution = pd.read_csv(test_file).set_index('index')
            # Test 1
            sol_er = solution[solution.columns[0:2]]
            sol_er.columns = mul_evt.er.columns
            sol_er.columns.name = 'Expected return'
            self.assertEqual(mul_evt.er, sol_er)
            # Test 2
            sol_ar = solution[solution.columns[3:5]]
            sol_ar.columns = mul_evt.ar.columns
            sol_ar.columns.name = 'Abnormal return'
            self.assertEqual(mul_evt.ar, sol_ar)
            # Test 3
            sol_car = solution[solution.columns[6:8]]
            sol_car.columns = mul_evt.car.columns
            sol_car.columns.name = 'Cum abnormal return'
            self.assertEqual(mul_evt.car, sol_car)
            # Test 4
            self.assertEqual(mul_evt.mean_er, solution['Mean ER'])
            self.assertEqual(mul_evt.mean_ar, solution['Mean AR'])
            self.assertEqual(mul_evt.mean_car, solution['Mean CAR'])

if __name__ == '__main__':
    suite = MultipleEventsTest().suite()
    unittest.TextTestRunner(verbosity=2).run(suite)

    # FinanceTest.delete_data()
