import unittest
import numpy as np
import pandas as pd
from datetime import datetime

from finance.utils import DataAccess
from finance.sim import MarketSimulator


class MarketSimulatorTest(unittest.TestCase):

    def setUp1(self):
        DataAccess('./data').empty_dirs()
        self.sim = MarketSimulator('./data')


    def suite(self):
        suite = unittest.TestSuite()
        suite.addTest(MarketSimulatorTest('test_values'))
        return suite

    def dfCompare(self, df1, df2):
        c = df1 == df2
        for idx, row in c.iterrows():
            if row[0] == False:
                return False
        return True

    def test_values(self):
        self.setUp1()

        self.sim.initial_cash = 1000000
        self.sim.simulate("orders.csv")

        # Test: Length of the DataFrame
        self.assertEqual(len(self.sim.portfolio), 240)
        self.assertEqual(len(self.sim.portfolio.columns), 1)

        # Test: Name of columns
        self.assertEqual(self.sim.portfolio.columns, 'Portfolio')
        self.assertEqual(self.sim.portfolio.index.name, 'Date')

        # Create a test DataFrame
        testdf = pd.DataFrame([0, 0, 0, 0, 0])
        testdf.index.name = 'Date'

        # ========================== HEAD TEST ==============================================
        testdf.columns = ['Portfolio']
        testdf.index = [datetime(2011, 1, 10), datetime(2011, 1, 11), datetime(2011, 1, 12),
                        datetime(2011, 1, 13), datetime(2011, 1, 14)]

        # Portfolio: Test True Positive
        testdf['Portfolio'] = [1000000, 998785, 1002925, 1004800, 1009360]
        self.assertTrue(self.dfCompare(testdf, self.sim.portfolio.head()))
        # Portfolio: Test True Negative
        testdf['Portfolio'] = [11000000, 998785, 1002925, 1004800, 1009360]
        self.assertFalse(self.dfCompare(testdf, self.sim.portfolio.head()))

        # Cash: Test True Positive
        testdf.columns = ['Cash']
        testdf['Cash'] = [490840, 490840, 490840, 429120, 429120]
        self.assertTrue(self.dfCompare(testdf, self.sim.cash.head()))
        # Cash: Test True Negative
        testdf['Cash'] = [490840, 490840, 490840, 429120, 1429120]
        self.assertFalse(self.dfCompare(testdf, self.sim.cash.head()))

        # ========================== TAIL TEST ==============================================
        testdf.columns = ['Portfolio']
        testdf.index = [datetime(2011, 12, 14), datetime(2011, 12, 15), datetime(2011, 12, 16),
                        datetime(2011, 12, 19), datetime(2011, 12, 20)]

        # Portfolio: Test True Positive
        testdf['Portfolio'] = [1114519, 1113031, 1115515, 1116931, 1133263]
        self.assertTrue(self.dfCompare(testdf, self.sim.portfolio.tail()))
        # Portfolio: Test True Negative
        testdf['Portfolio'] = [1114519, 1113031, 1115515, 1116931, 1133264]
        self.assertFalse(self.dfCompare(testdf, self.sim.portfolio.tail()))

        # Cash: Test True Positive
        testdf.columns = ['Cash']
        testdf['Cash'] = [662311, 662311, 662311, 662311, 1133263]
        self.assertTrue(self.dfCompare(testdf, self.sim.cash.tail()))
        # Cash: Test True Negative
        testdf['Cash'] = [662311, 662311, 662311, 662311, 1133264]
        self.assertFalse(self.dfCompare(testdf, self.sim.cash.tail()))


if __name__ == '__main__':
    suite = MarketSimulatorTest().suite()
    unittest.TextTestRunner(verbosity=2).run(suite)

    DataAccess('./data').empty_dirs()