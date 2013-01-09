import unittest
import numpy as np
import pandas as pd
import numpy.testing as np_test
import pandas.util.testing as pd_test

from finance.utils import DataAccess
from finance.utils import Calculator
from finance.sim import MarketSimulator

class CalculatorValues(unittest.TestCase):

    def setUp1(self):
        DataAccess.path = 'data'
        self.data_access = DataAccess()
        self.data_access.empty_dirs()

    def suite(self):
        suite = unittest.TestSuite()
        suite.addTest(CalculatorValues('test_assets'))
        suite.addTest(CalculatorValues('test_time_value_of_money'))

        suite.addTest(CalculatorValues('test_ret'))
        suite.addTest(CalculatorValues('test_returns'))
        suite.addTest(CalculatorValues('test_sharpe_ratio'))
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
        pd_test.assert_series_equal(solution['R(t)'], simple_returns)
        # Test 2
        cc_returns = Calculator.returns(data, cc=True)
        pd_test.assert_series_equal(solution['r(t)'], cc_returns)
        # Test 3
        simple_returns_2 = Calculator.returns(data, basedOn=2)
        pd_test.assert_series_equal(solution['R2(t)'], simple_returns_2)
        # Test 4
        cc_returns_2 = Calculator.returns(data, basedOn=2, cc=True)
        pd_test.assert_series_equal(solution['r2(t)'], cc_returns_2)
        # Test 5
        fv = Calculator.FV(PV=1, R=simple_returns, ret_list=True)
        pd_test.assert_series_equal(solution['FV'], fv)
        # Test 6
        pv = Calculator.PV(FV=fv[-1], R=simple_returns, ret_list=True)
        pd_test.assert_series_equal(solution['FV'], pv)

    def test_time_value_of_money(self):
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

    def test_ret(self):
        '''
        Tests the input and output types
        '''
        d1_array = np.array([1,2,3,4,5])
        d1_array2 = np.array([5,4,3,2,1])
        d2_array = np.array([d1_array, d1_array2]).T

        # Input is numpy.ndarray of 1 dimmension => Returns float
        ans = Calculator.ret(np.array(d1_array))
        self.assertEquals(ans, 4)
        # Input is numpy.ndarray of 2 dimmensions => Returns np.ndarray
        ans = Calculator.ret(d2_array)
        np_test.assert_array_equal(ans, [4, -0.8])
        # Input is pandas.Series => Returns float
        ans = Calculator.ret(pd.Series(d1_array))
        self.assertEquals(ans, 4)
        # Input is pandas.TimeSeries  => Returns float
        ans = Calculator.ret(pd.TimeSeries(d1_array))
        self.assertEquals(ans, 4)
        # Input is pandas.DataFrame with col parameter => Returns float
        df = pd.DataFrame(d2_array, columns=['c1', 'c2'], index=[1,2,3,4,5])
        ans = Calculator.ret(df, col='c1')
        self.assertEquals(ans, 4)
        ans = Calculator.ret(df, col='c2')
        self.assertEquals(ans, -0.8)
        # Input is pandas.DataFrame without col parameter => Return pd.DataFrame
        ans = Calculator.ret(df)
        sol = pd.Series([4, -0.8], index=['c1', 'c2'], name='Total Returns')
        pd_test.assert_series_equal(ans, sol)


    def test_returns(self):
        d1_array_1 = np.array([1,1.5,3,4,4.3])
        d1_array_2 = np.array([5,4.3,3,3.5,1])
        d2_array = np.array([d1_array_1, d1_array_2]).T
        
        sol_d1_array_1 = np.array([0, 0.5, 1, 0.33333333, 0.075])
        d1_array_2_dr = np.array([ 0., -0.14, -0.30232558, 0.16666667, -0.71428571])
        d2_array_dr = np.array([sol_d1_array_1, d1_array_2_dr]).T

        # Test: Input is numpy.ndarray of 1 dimmension
        ans = Calculator.returns(d1_array_1)
        np_test.assert_array_almost_equal(ans, sol_d1_array_1, 5)

        # Test: Input is numpy.ndarray of 2 dimmension 2
        ans = Calculator.returns(d2_array)
        np_test.assert_array_almost_equal(ans, d2_array_dr, 5)

        # Test: Input is pandas.Series
        ser = pd.Series(d1_array_1, name='TEST')
        ans = Calculator.returns(ser)
        sol = pd.Series(sol_d1_array_1, index=ser.index, name='TEST Daily Returns')
        pd_test.assert_series_equal(ans, sol)
        
        # Test: Input is pandas.DataFrame and gives col parameter
        df = pd.DataFrame(d2_array, columns=['c1', 'c2'])
        ans = Calculator.returns(df, col='c1')
        sol = pd.Series(sol_d1_array_1, index=df.index, name='c1 Daily Returns')
        pd_test.assert_series_equal(ans, sol)

        ans = Calculator.returns(df, col='c2')
        sol = pd.Series(d1_array_2_dr, index=df.index, name='c2 Daily Returns')
        pd_test.assert_series_equal(ans, sol)

        # Test: Input is pandas.DataFrame and do not gives col parameter
        ans = Calculator.returns(df)
        sol = pd.DataFrame(d2_array_dr, index=df.index, columns=df.columns)
        pd_test.assert_frame_equal(ans, sol)

    def test_sharpe_ratio(self):
        d1_array = np.array([1,1.5,3,4,4.3])
        d1_array_2 = np.array([5,4.3,3,3.5,1])
        d2_array = np.array([d1_array, d1_array_2]).T

        # Test: Input is np.array of 1 dimmension
        ans = Calculator.sharpe_ratio(d1_array)
        self.assertAlmostEquals(ans, 2.38842, 5)

        # Test: Input is np.array of 2 dimmensions
        ans = Calculator.sharpe_ratio(d2_array)
        sol = np.array([2.38842482, -1.4708528])
        np_test.assert_array_almost_equal(ans, sol, 5)

        # Test: Input is pandas.TimeSeries/Series
        ans = Calculator.ret(pd.TimeSeries(d1_array))
        self.assertAlmostEquals(ans, 3.299999, 5)
        ans = Calculator.ret(pd.Series(d1_array))
        self.assertAlmostEquals(ans, 3.299999, 5)

        # Test: Input is pandas.DataFrame with col parameter
        df = pd.DataFrame(d2_array, columns=['c1', 'c2'])
        ans = Calculator.ret(df, col='c1')
        self.assertAlmostEquals(ans, 3.299999, 5)
        ans = Calculator.ret(df, col='c2')
        self.assertEquals(ans, -0.8)

        # Test: Input is pandas.DataFrame without col parameter
        ans = Calculator.ret(df)
        sol = pd.Series([3.299999, -0.8], index=['c1', 'c2'], name='Shape Ratios')
        pd_test.assert_series_equal(ans, sol)


if __name__ == '__main__':
    suite = CalculatorValues().suite()
    unittest.TextTestRunner(verbosity=2).run(suite)

    # DataAccess().empty_dirs(delete=True)
