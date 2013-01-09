import unittest
import numpy as np
import pandas as pd
from datetime import datetime
from finance.test import FinanceTest

from finance.utils import DataAccess
from finance.sim import MarketSimulator


class MarketSimulatorTest(FinanceTest):

    def suite(self):
        suite = unittest.TestSuite()
        suite.addTest(MarketSimulatorTest('test_1'))
        return suite

    def test_1(self):
        '''
        Loads solution from csv file and test the values
        Tests
        -----
            1. Name of the solution Series: cash, equities, portfolio
            2. Values of the solution Series: cash, equities, portfolio
        '''
        # Set up
        self.setUpDataAccess(eraseData=False, eraseCache=True)
        solution = pd.read_csv('docs/Test1.csv')
        solution = solution.set_index(pd.to_datetime(solution['Date']))

        simulator = MarketSimulator()
        simulator.initial_cash = 1000000
        simulator.load_trades("orders.csv")
        simulator.simulate()  

        # Test 1
        self.assertEqual(simulator.cash.name, 'Cash')
        self.assertEqual(simulator.equities.name, 'Equities value')
        self.assertEqual(simulator.portfolio.name, 'Portfolio value')
        # Test 2
        self.assertEqual(simulator.cash, solution['Cash'])
        self.assertEqual(simulator.equities, solution['Equities value'])
        self.assertEqual(simulator.portfolio, solution['Portfolio value'])

if __name__ == '__main__':
    suite = MarketSimulatorTest().suite()
    unittest.TextTestRunner(verbosity=2).run(suite)

    # FinanceTest.delete_data()