import unittest
import numpy as np
import pandas as pd
import pandas.util.testing as pd_test
from datetime import datetime
from finance.utils import DataAccess
from finance.sim import MarketSimulator


class MarketSimulatorTest(unittest.TestCase):

    def setUp1(self):
        DataAccess('./data').empty_dirs()
        self.sim = MarketSimulator('./data')

    def suite(self):
        suite = unittest.TestSuite()
        suite.addTest(MarketSimulatorTest('test_success'))
        return suite

    def test_success(self):
        self.setUp1()

        self.sim.initial_cash = 1000000
        self.sim.simulate("orders.csv")

        # Test: Length of the DataFrame
        self.assertEqual(len(self.sim.portfolio), 240)
        self.assertEqual(len(self.sim.portfolio.columns), 1)
        # Test: Name of columns
        self.assertEqual(self.sim.portfolio.columns, 'Portfolio')
        self.assertEqual(self.sim.portfolio.index.name, 'Date')

        # Test: Values - Create a test DataFrame
        testdf = pd.DataFrame([0.0, 0.0, 0.0, 0.0, 0.0])
        testdf.index.name = 'Date'

        # Test: Values: HEAD()
        testdf.index = [datetime(2011, 1, 10), datetime(2011, 1, 11), datetime(2011, 1, 12),
                        datetime(2011, 1, 13), datetime(2011, 1, 14)]
        # Test: Values: HEAD(): portfolio
        testdf.columns = ['Portfolio']
        testdf['Portfolio'] = [1000000.0, 998785, 1002925, 1004800, 1009360]
        pd_test.assert_frame_equal(testdf, self.sim.portfolio.head())
        # Test: Values: HEAD(): cash
        testdf.columns = ['Cash']
        testdf['Cash'] = [490840.0, 490840, 490840, 429120, 429120]
        pd_test.assert_frame_equal(testdf, self.sim.cash.head())

        # Test: Values: TAIL()
        testdf.index = [datetime(2011, 12, 14), datetime(2011, 12, 15), datetime(2011, 12, 16),
                        datetime(2011, 12, 19), datetime(2011, 12, 20)]
        # Test: Values: TAIL(): portfolio
        testdf.columns = ['Portfolio']
        testdf['Portfolio'] = [1114519.0, 1113031, 1115515, 1116931, 1133263]
        pd_test.assert_frame_equal(testdf, self.sim.portfolio.tail())
        # Test: Values: TAIL(): cash
        testdf.columns = ['Cash']
        testdf['Cash'] = [662311.0, 662311, 662311, 662311, 1133263]
        pd_test.assert_frame_equal(testdf, self.sim.cash.tail())

if __name__ == '__main__':
    suite = MarketSimulatorTest().suite()
    unittest.TextTestRunner(verbosity=2).run(suite)

    DataAccess('./data').empty_dirs()