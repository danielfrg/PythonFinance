import unittest
import numpy as np
import numpy.testing as np_test
import pandas as pd
import pandas.util.testing as pd_test
from finance.utils import DataAccess
from finance.utils import BasicUtils
from finance.sim import MarketSimulator

class BasicUtilsTest(unittest.TestCase):

    def setUp1(self):
        DataAccess('./data').empty_dirs()
        self.da = DataAccess('./data')

    def suite(self):
        suite = unittest.TestSuite()
        suite.addTest(BasicUtilsTest('test_total_return'))
        suite.addTest(BasicUtilsTest('test_sharpe_ratio'))
        suite.addTest(BasicUtilsTest('test_daily_return'))
        return suite

    def test_total_return(self):
        sim = MarketSimulator('./data')
        sim.initial_cash = 1000000
        sim.simulate("../../sim/test/orders.csv")

        # Test: Input is pandas.Series
        tr = BasicUtils.total_return(sim.portfolio['Portfolio'])
        self.assertEquals(tr, 0.1332629999999999)
        # Test: Input is numpy.array
        tr = BasicUtils.total_return(sim.portfolio['Portfolio'].values)
        self.assertEquals(tr, 0.1332629999999999)

    def test_daily_return(self):
        # Test: Input is numpy.array
        arr = np.array([1,1.5,3])
        ans = BasicUtils.daily_returns(arr)
        self.assertEquals(type(ans), np.ndarray)
        sol = np.array([0, 0.5, 1])
        np_test.assert_array_equal(ans, sol)
        # Test: Input is pandas.Series
        s = pd.Series([1,1.5,3], index=[2,3,4])
        ans = BasicUtils.daily_returns(s)
        sol = pd.Series([0, 0.5, 1], index=s.index)
        pd_test.assert_series_equal(ans, sol)
        # Test: Input is pandas.DataFrame
        d = pd.DataFrame([[1,1.5,3], [4,4,5]], columns=['c1', 'c2', 'c3'])
        ans = BasicUtils.daily_returns(d)
        sol = pd.DataFrame([[0.0,0.0,0.0], [3, 1.66667, 0.666667]], index=d.index, columns=d.columns)
        pd_test.assert_frame_equal(ans, sol)

    def test_sharpe_ratio(self):
        sim = MarketSimulator('./data')
        sim.initial_cash = 1000000
        sim.simulate("../../sim/test/orders.csv")

        # Test: give pd.DataFrame
        # Test: extraAnswers=False
        sr = BasicUtils.sharpe_ratio(sim.portfolio)
        self.assertEquals(sr, 1.1825359272456812)
        # Test: extraAnswers=True
        sr = BasicUtils.sharpe_ratio(sim.portfolio, extraAnswers=True)
        self.assertEquals(sr['sharpe_ratio'], 1.1825359272456812)
        self.assertEquals(sr['std'], 0.0071658104790118396)
        self.assertEquals(sr['mean'], 0.00054698326727656884)

        # Test: give np.array
        # Test: extraAnswers=False
        sr = BasicUtils.sharpe_ratio(sim.portfolio.values)
        self.assertAlmostEquals(sr, 1.1825359272456812, 2)
        # Test: extraAnswers=True
        sr = BasicUtils.sharpe_ratio(sim.portfolio, extraAnswers=True)
        self.assertAlmostEquals(sr['sharpe_ratio'], 1.1825359272456812, 2)
        self.assertAlmostEquals(sr['std'], 0.0071658104790118396, 2)
        self.assertAlmostEquals(sr['mean'], 0.00054698326727656884, 2)

if __name__ == '__main__':
    suite = BasicUtilsTest().suite()
    unittest.TextTestRunner(verbosity=2).run(suite)

    DataAccess('./data').empty_dirs(delete=True)