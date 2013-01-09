import unittest
import os, inspect
import numpy as np
import pandas as pd
from finance.test import FinanceTest

from finance.utils import Calculator

class CalculatorValuesTest(FinanceTest):
    '''
    Tests the values of the functions
    '''

    def suite(self):
        
        suite = unittest.TestSuite()
        suite.addTest(CalculatorValuesTest('test_assets'))
        suite.addTest(CalculatorValuesTest('test_tvm'))
        return suite

    def test_assets(self):
        '''
        Tests
        -----
            1. Calculator.returns w/ basedOn=1 cc=False
            2. Calculator.returns w/ basedOn=1 cc=True
            3. Calculator.returns w/ basedOn=2 cc=False
            4. Calculator.returns w/ basedOn=2 cc=True
            5. Calculator.FV w/ R=list ret_list=True
            6. Calculator.PV w/ R=list ret_list=True
        '''
        # Load Data
        self_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        tests = ['Calculator_Assets_1.csv']
        tests = [os.path.join(self_dir, 'docs', test) for test in tests]

        for test_file in tests:
            # Set up
            solution = pd.read_csv(test_file).set_index('Date').fillna(value=0)
            data = solution['Adj. Close']

            # Test 1
            simple_returns = Calculator.returns(data)
            self.assertEqual(solution['Adj. Close returns'], simple_returns)
            # Test 2
            cc_returns = Calculator.returns(data, cc=True)
            self.assertEqual(solution['Adj. Close CC returns'], cc_returns)
            # Test 3
            simple_returns_2 = Calculator.returns(data, basedOn=2)
            self.assertEqual(solution['Adj. Close returns (2)'], simple_returns_2)
            # Test 4
            cc_returns_2 = Calculator.returns(data, basedOn=2, cc=True)
            self.assertEqual(solution['Adj. Close CC returns (2)'], cc_returns_2)
            # Test 5
            fv = Calculator.FV(PV=1, R=simple_returns, ret_list=True)
            self.assertEqual(solution['Future value'], fv)
            # Test 6
            pv = Calculator.PV(FV=fv[-1], R=simple_returns, ret_list=True)
            pv_sol = solution['Future value']
            pv_sol.name = 'Present value'
            self.assertEqual(solution['Future value'], pv)

    def test_tvm(self):
        '''
        Tests
        -----
            1. FV w/ PV, R, n, m and ret_list=False
            2. PV w/ PV, R, n, m and ret_list=False
            3. R w/ PV, FV, n, m
            4. n w/ PV, FV, R, m
            5. ear w/ R, m
        '''
        self_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        tests = ['Calculator_TVM_1.csv', 'Calculator_TVM_2.csv', 
                'Calculator_TVM_3.csv']
        tests = [os.path.join(self_dir, 'docs',test) for test in tests]

        for test_file in tests:
            # Set up
            solution = pd.read_csv(test_file)

            for idx, row in solution.iterrows():
                # Test 1
                FV = Calculator.FV(PV=row['PV'], R=row['R'], n=row['n'], m=row['m'])
                self.assertAlmostEquals(FV, row['FV'], 4)
                # Test 2
                PV = Calculator.PV(FV=row['FV'], R=row['R'], n=row['n'], m=row['m'])
                self.assertAlmostEquals(PV, row['PV'], 4)
                # Test 3
                R = Calculator.R(PV=row['PV'], FV=row['FV'], n=row['n'], m=row['m'])
                self.assertAlmostEquals(R, row['R'], 4)
                # Test 4
                n = Calculator.n(PV=row['PV'], FV=row['FV'], R=row['R'], m=row['m'])
                self.assertAlmostEquals(n, row['n'], 4)
                # Test 5
                ear = Calculator.eff_ret(R=row['R'], m=row['m'])
                self.assertAlmostEquals(ear, row['EAR'], 4, "R(%s),m(%s)" % (row['R'], row['m']))

if __name__ == '__main__':
    suite = CalculatorValuesTest().suite()
    unittest.TextTestRunner(verbosity=2).run(suite)
