import unittest
import numpy as np
import pandas as pd
from finance.test import FinanceTest

from finance.utils import Calculator

class CalculatorTestValues(FinanceTest):
    '''
    Tests the values of the functions
    '''

    def suite(self):
        suite = unittest.TestSuite()
        suite.addTest(CalculatorTestValues('test_assets'))
        suite.addTest(CalculatorTestValues('test_tvm'))
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
        solution = pd.read_csv('CalculatorTest_Assets_1.csv').set_index('Date').fillna(value=0)
        data = solution['Adj. Close']
        # Test 1
        simple_returns = Calculator.returns(data)
        self.assertSeriesEqual(solution['R(t)'], simple_returns)
        # Test 2
        cc_returns = Calculator.returns(data, cc=True)
        self.assertSeriesEqual(solution['r(t)'], cc_returns)
        # Test 3
        simple_returns_2 = Calculator.returns(data, basedOn=2)
        self.assertSeriesEqual(solution['R2(t)'], simple_returns_2)
        # Test 4
        cc_returns_2 = Calculator.returns(data, basedOn=2, cc=True)
        self.assertSeriesEqual(solution['r2(t)'], cc_returns_2)
        # Test 5
        fv = Calculator.FV(PV=1, R=simple_returns, ret_list=True)
        self.assertSeriesEqual(solution['FV'], fv)
        # Test 6
        pv = Calculator.PV(FV=fv[-1], R=simple_returns, ret_list=True)
        self.assertSeriesEqual(solution['FV'], pv)

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
        tests = ['CalculatorTest_TVM_1.csv', 'CalculatorTest_TVM_2.csv', 
                'CalculatorTest_TVM_3.csv'] #, 'CalculatorTest_TVM_4.csv']

        for test_file in tests:
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
    suite = CalculatorTestValues().suite()
    unittest.TextTestRunner(verbosity=2).run(suite)
