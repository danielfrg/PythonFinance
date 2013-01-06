import unittest
import numpy as np
import pandas as pd
import numpy.testing as np_test
import pandas.util.testing as pd_test

from finance.utils import DataAccess
from finance.utils import Calculator
from finance.sim import MarketSimulator

class BasicUtilsTest(unittest.TestCase):

    def setUp1(self):
        DataAccess.path = 'data'
        self.data_access = DataAccess()
        self.data_access.empty_dirs()

    def suite(self):
        suite = unittest.TestSuite()
        suite.addTest(BasicUtilsTest('test_present_and_future_value'))
        suite.addTest(BasicUtilsTest('test_rates_and_n'))
        # suite.addTest(BasicUtilsTest('test_total_return'))
        # suite.addTest(BasicUtilsTest('test_daily_return'))
        # suite.addTest(BasicUtilsTest('test_sharpe_ratio'))
        return suite

    def test_rates_and_n(self):
        # Test: Rate from PV and FV
        ans = Calculator.R(PV=1000, FV=1030, n=1)
        self.assertAlmostEquals(0.03, ans, 4)
        ans = Calculator.R(PV=1000, FV=1159.27, n=5)
        self.assertAlmostEquals(0.03, ans, 4)
        ans = Calculator.R(PV=1000, FV=1343.92, n=10)
        self.assertAlmostEquals(0.03, ans, 4)

        # Test Efective Annual Rate
        ans = Calculator.ear(R=0.1, m=1)
        self.assertAlmostEquals(0.1, ans, 4)
        ans = Calculator.ear(R=0.1, m=4)
        self.assertAlmostEquals(0.1038, ans, 4)
        ans = Calculator.ear(R=0.1, m=52)
        self.assertAlmostEquals(0.1051, ans, 4)
        ans = Calculator.ear(R=0.1, m=365)
        self.assertAlmostEquals(0.105155, ans, 5)
        ans = Calculator.ear(R=0.1, m=float('inf'))
        self.assertAlmostEquals(0.105170, ans, 5)

        # Test n
        ans = Calculator.n(PV=1000, FV=1030, R=0.03)
        self.assertAlmostEquals(1, ans, 4)
        ans = Calculator.n(PV=1000, FV=1159.27, R=0.03)
        self.assertAlmostEquals(5, ans, 2)
        ans = Calculator.n(PV=1000, FV=1343.92, R=0.03)
        self.assertAlmostEquals(10, ans, 2)



    def test_present_and_future_value(self):
        # Test Future Value with NO compounding frequency
        ans = Calculator.FV(PV=1000, R=0.03, n=1)
        self.assertEquals(1030, ans)
        ans = Calculator.FV(PV=1000, R=0.03, n=5)
        self.assertAlmostEquals(1159.27, ans, 2)
        ans = Calculator.FV(PV=1000, R=0.03, n=10)
        self.assertAlmostEquals(1343.92, ans, 2)

        # Test Present Value with NO compounding frequency: Inverse of the previous
        ans = Calculator.PV(FV=1030, R=0.03, n=1)
        self.assertEquals(1000, ans)
        ans = Calculator.PV(FV=1159.27, R=0.03, n=5)
        self.assertAlmostEquals(1000, ans, 2)
        ans = Calculator.PV(FV=1343.92, R=0.03, n=10)
        self.assertAlmostEquals(1000, ans, 2)

        # Test Future Value: with compounding frequency
        ans = Calculator.FV(PV=1000, R=0.1, n=1, m=1)
        self.assertEquals(1100, ans)
        ans = Calculator.FV(PV=1000, R=0.1, n=1, m=4)
        self.assertAlmostEquals(1103.81, ans, 2)
        ans = Calculator.FV(PV=1000, R=0.1, n=1, m=52)
        self.assertAlmostEquals(1105.06, ans, 2)
        ans = Calculator.FV(PV=1000, R=0.1, n=1, m=365)
        self.assertAlmostEquals(1105.16, ans, 2)
        ans = Calculator.FV(PV=1000, R=0.1, n=1, m=float('inf'))
        self.assertAlmostEquals(1105.17, ans, 2)


        # Test Present Value: with compounding frequency: Inverse of the previous
        ans = Calculator.PV(FV=1100, R=0.1, n=1, m=1)
        self.assertAlmostEquals(1000, ans, 2)
        ans = Calculator.PV(FV=1103.81, R=0.1, n=1, m=4)
        self.assertAlmostEquals(1000, ans, 2)
        ans = Calculator.PV(FV=1105.06, R=0.1, n=1, m=52)
        self.assertAlmostEquals(1000, ans, 2)
        ans = Calculator.PV(FV=1105.16, R=0.1, n=1, m=365)
        self.assertAlmostEquals(1000, ans, 2)
        ans = Calculator.PV(FV=1105.17, R=0.1, n=1, m=float('inf'))
        self.assertAlmostEquals(1000, ans, 2)

    def test_total_return(self):
        d1_array = np.array([1,2,3,4,5])
        d2_array = np.array([   [1,5],
                                [2,4],
                                [3,3],
                                [4,2],
                                [5,1]])

        # Test: Input is numpy.ndarray of 1 dimmension
        ans = Calculator.total_return(np.array(d1_array))
        self.assertEquals(ans, 4)

        # Test: Input is numpy.ndarray of 2 dimmensions
        ans = Calculator.total_return(d2_array)
        np_test.assert_array_equal(ans, [4, -0.8])

        # Test: Input is pandas.TimeSeries/Series
        ans = Calculator.total_return(pd.TimeSeries(d1_array))
        self.assertEquals(ans, 4)
        ans = Calculator.total_return(pd.Series(d1_array))
        self.assertEquals(ans, 4)

        # Test: Input is pandas.DataFrame with col parameter
        df = pd.DataFrame(d2_array, columns=['c1', 'c2'], index=[1,2,3,4,5])
        ans = Calculator.total_return(df, 'c1')
        self.assertEquals(ans, 4)
        ans = Calculator.total_return(df, 'c2')
        self.assertEquals(ans, -0.8)

        # Test: Input is pandas.DataFrame without col parameter
        ans = Calculator.total_return(df)
        sol = pd.Series([4, -0.8], index=['c1', 'c2'], name='Total Returns')
        pd_test.assert_series_equal(ans, sol)

    def test_daily_return(self):
        d1_array_1 = np.array([1,1.5,3,4,4.3])
        d1_array_2 = np.array([5,4.3,3,3.5,1])
        d2_array = np.array([d1_array_1, d1_array_2]).T
        
        d1_array_1_dr = np.array([0, 0.5, 1, 0.33333333, 0.075])
        d1_array_2_dr = np.array([ 0., -0.14, -0.30232558, 0.16666667, -0.71428571])
        d2_array_dr = np.array([d1_array_1_dr, d1_array_2_dr]).T

        # Test: Input is numpy.ndarray of 1 dimmension
        ans = Calculator.daily_returns(d1_array_1)
        np_test.assert_array_almost_equal(ans, d1_array_1_dr, 5)
        ans = Calculator.daily_returns(d1_array_2)
        np_test.assert_array_almost_equal(ans, d1_array_2_dr, 5)

        # Test: Input is numpy.ndarray of 2 dimmension 2
        ans = Calculator.daily_returns(d2_array)
        np_test.assert_array_almost_equal(ans, d2_array_dr, 5)

        # Test: Input is pandas.Series
        ser = pd.Series(d1_array_1, name='TEST')
        ans = Calculator.daily_returns(ser)
        sol = pd.Series(d1_array_1_dr, index=ser.index, name='TEST Daily Returns')
        pd_test.assert_series_equal(ans, sol)
        
        # Test: Input is pandas.DataFrame and gives col parameter
        df = pd.DataFrame(d2_array, columns=['c1', 'c2'])
        ans = Calculator.daily_returns(df, col='c1')
        sol = pd.Series(d1_array_1_dr, index=df.index, name='c1 Daily Returns')
        pd_test.assert_series_equal(ans, sol)

        ans = Calculator.daily_returns(df, col='c2')
        sol = pd.Series(d1_array_2_dr, index=df.index, name='c2 Daily Returns')
        pd_test.assert_series_equal(ans, sol)

        # Test: Input is pandas.DataFrame and do not gives col parameter
        ans = Calculator.daily_returns(df)
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
        ans = Calculator.total_return(pd.TimeSeries(d1_array))
        self.assertAlmostEquals(ans, 3.299999, 5)
        ans = Calculator.total_return(pd.Series(d1_array))
        self.assertAlmostEquals(ans, 3.299999, 5)

        # Test: Input is pandas.DataFrame with col parameter
        df = pd.DataFrame(d2_array, columns=['c1', 'c2'])
        ans = Calculator.total_return(df, 'c1')
        self.assertAlmostEquals(ans, 3.299999, 5)
        ans = Calculator.total_return(df, 'c2')
        self.assertEquals(ans, -0.8)

        # Test: Input is pandas.DataFrame without col parameter
        ans = Calculator.total_return(df)
        sol = pd.Series([3.299999, -0.8], index=['c1', 'c2'], name='Shape Ratios')
        pd_test.assert_series_equal(ans, sol)


if __name__ == '__main__':
    suite = BasicUtilsTest().suite()
    unittest.TextTestRunner(verbosity=2).run(suite)

    # DataAccess().empty_dirs(delete=True)
