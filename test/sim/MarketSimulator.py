import unittest
import os, inspect
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
        self.setUpDataAccess()

        self_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        tests = ['Test_1.csv']
        tests = [os.path.join(self_dir, 'docs', test) for test in tests]

        orders = ['orders_1.csv']
        orders = [os.path.join(self_dir, 'docs', order) for order in orders]

        for test_file, order in zip(tests, orders):
            solution = pd.read_csv(test_file)
            solution = solution.set_index(pd.to_datetime(solution['Date']))

            simulator = MarketSimulator()
            simulator.initial_cash = 1000000
            simulator.load_trades(order)
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