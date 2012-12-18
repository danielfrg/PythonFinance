# Test imports
import unittest
import numpy as np
import pandas as pd
from datetime import datetime

# General imports
from finance.utils import DataAccess
from finance.sim import MarketSimulator


class TestMarketSimulator(unittest.TestCase):
    def setUp0(self):
        self.da = DataAccess('./data')
        self.da.empty_dirs()
        self.sim = MarketSimulator('./data')

    def setUp1(self):
        self.sim = MarketSimulator('./data')

    def dfCompare(self, df1, df2):
        c = df1 == df2
        for idx, row in c.iterrows():
            if row[0] == False:
                return False
        return True

    def testSimulationValues(self):
        self.setUp1()

        self.sim.initial_cash = 1000000
        self.sim.simulate("orders.csv")

        # Test the length of the DataFrame, Also the name of columns
        self.assertEqual(len(self.sim.portfolio), 240)
        self.assertEqual(len(self.sim.portfolio.columns), 1)
        self.assertEqual(self.sim.portfolio.columns, 'Portfolio')
        self.assertEqual(self.sim.portfolio.index.name, 'Date')

        # Create a test DataFrame
        testdf = pd.DataFrame([0, 0, 0, 0, 0])
        testdf.index.name = 'Date'

        # ========================== HEAD TEST ==============================================

        # Portfolio: Test True Positive
        testdf.columns = ['Portfolio']
        testdf.index = [datetime(2011, 1, 10), datetime(2011, 1, 11), datetime(2011, 1, 12),
                        datetime(2011, 1, 13), datetime(2011, 1, 14)]
        testdf['Portfolio'] = [1000000, 998785, 1002925, 1004800, 1009360]
        self.assertEqual(self.dfCompare(testdf, self.sim.portfolio.head()), True)
        # Portfolio: Test True Negative
        testdf['Portfolio'] = [11000000, 998785, 1002925, 1004800, 1009360]
        self.assertEqual(self.dfCompare(testdf, self.sim.portfolio.head()), False)
        # Portfolio: Test True Negative
        testdf['Portfolio'] = [1000000, 1998785, 1002925, 1004800, 1009360]
        self.assertEqual(self.dfCompare(testdf, self.sim.portfolio.head()), False)

        # Cash: Test True Positive
        testdf.columns = ['Cash']
        testdf['Cash'] = [490840, 490840, 490840, 429120, 429120]
        self.assertEqual(self.dfCompare(testdf, self.sim.cash.head()), True)
        # Cash: Test True Negative
        testdf['Cash'] = [490840, 490840, 490840, 429120, 1429120]
        self.assertEqual(self.dfCompare(testdf, self.sim.cash.head()), False)

        # ========================== TAIL TEST ==============================================

        # Portfolio: Test True Positive
        testdf.columns = ['Portfolio']
        testdf.index = [datetime(2011, 12, 14), datetime(2011, 12, 15), datetime(2011, 12, 16),
                        datetime(2011, 12, 19), datetime(2011, 12, 20)]
        testdf['Portfolio'] = [1114519, 1113031, 1115515, 1116931, 1133263]
        self.assertEqual(self.dfCompare(testdf, self.sim.portfolio.tail()), True)
        # Portfolio: Test True Negative
        testdf['Portfolio'] = [1114519, 1113031, 1115515, 1116931, 1133264]
        self.assertEqual(self.dfCompare(testdf, self.sim.portfolio.tail()), False)

        # Cash: Test True Positive
        testdf.columns = ['Cash']
        testdf['Cash'] = [662311, 662311, 662311, 662311, 1133263]
        self.assertEqual(self.dfCompare(testdf, self.sim.cash.tail()), True)
        # Cash: Test True Negative
        testdf['Cash'] = [662311, 662311, 662311, 662311, 1133264]
        self.assertEqual(self.dfCompare(testdf, self.sim.cash.tail()), False)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMarketSimulator)
    unittest.TextTestRunner(verbosity=2).run(suite)

    DataAccess('./data').empty_dirs(delete=True)