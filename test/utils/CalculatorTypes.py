import unittest
import numpy as np
import pandas as pd
from finance.test import FinanceTest

from finance.utils import Calculator

class CalculatorTypesTest(FinanceTest):
    '''
    Tests output types for different input types of the functions
    If there outputs are Series or DataFrames checks its column names
    Also tests very basic output values
    '''

    def suite(self):
        suite = unittest.TestSuite()
        suite.addTest(CalculatorTypesTest('test_ret'))
        suite.addTest(CalculatorTypesTest('test_returns'))
        suite.addTest(CalculatorTypesTest('test_sharpe_ratio'))
        return suite

    def test_ret(self):
        # Variables
        array = np.array([1,2,3,4,5])
        array_2 = np.array([5,4,3,2,1])
        matrix = np.array([array, array_2]).T
        series = pd.Series(array, index=[5,7,8,10,11])
        time_series = pd.TimeSeries(array)
        df = pd.DataFrame(matrix, columns=['c1', 'c2'], index=[5,7,8,10,11])

        # Input is numpy.ndarray of 1 dimmension => float
        ans = Calculator.ret(array)
        self.assertFloat(ans)
        self.assertEqual(ans, 4)
        # Input is numpy.ndarray of 2 dimmensions => np.ndarray
        ans = Calculator.ret(matrix)
        self.assertArray(ans)
        self.assertEqual(ans, np.array([4, -0.8]))
        # Input is pandas.Series => float
        ans = Calculator.ret(series)
        self.assertFloat(ans)
        self.assertEqual(ans, 4)
        # Input is pandas.TimeSeries  => float
        ans = Calculator.ret(time_series)
        self.assertFloat(ans)
        self.assertEqual(ans, 4)
        # Input is pandas.DataFrame with col parameter => float
        ans = Calculator.ret(df, col='c1')
        self.assertFloat(ans)
        self.assertEqual(ans, 4)
        # --
        ans = Calculator.ret(df, col='c2')
        self.assertFloat(ans)
        self.assertEqual(ans, -0.8)
        # Input is pandas.DataFrame without col parameter => Return pd.Series
        ans = Calculator.ret(df)
        self.assertSeries(ans)
        sol = pd.Series([4, -0.8], index=['c1', 'c2'], name='Total Returns')
        self.assertEqual(ans, sol)


    def test_returns(self):
        # Variables
        array_1 = np.array([1,1.5,3,4,4.3])
        array_2 = np.array([5,4.3,3,3.5,1])
        matrix = np.array([array_1, array_2]).T
        ser = pd.Series(array_1, name='TEST')
        df = pd.DataFrame(matrix, columns=['c1', 'c2'])
        
        sol_array_1 = np.array([0, 0.5, 1, 0.33333333, 0.075])
        sol_array_2 = np.array([ 0., -0.14, -0.30232558, 0.16666667, -0.71428571])
        sol_matrix = np.array([sol_array_1, sol_array_2]).T

        # Input is numpy.array of 1 dimmension => np.ndarray
        ans = Calculator.returns(array_1)
        self.assertArray(ans)
        self.assertEqual(ans, sol_array_1, 5)
        # Input is numpy.ndarray of 2 dimmension 2 => np.ndarray
        ans = Calculator.returns(matrix) 
        self.assertArray(ans)
        self.assertEqual(ans, sol_matrix, 5)
        # Input is pandas.Series => pd.Series
        ans = Calculator.returns(ser)
        self.assertSeries(ans)
        sol = pd.Series(sol_array_1, index=ser.index, name='TEST returns')
        self.assertEqual(ans, sol)
        # Input is pandas.DataFrame with col parameter => pd.Series
        ans = Calculator.returns(df, col='c1')
        self.assertSeries(ans)
        sol = pd.Series(sol_array_1, index=df.index, name='c1 returns')
        self.assertEqual(ans, sol)
        # --
        ans = Calculator.returns(df, col='c2')
        self.assertSeries(ans)
        sol = pd.Series(sol_array_2, index=df.index, name='c2 returns')
        self.assertEqual(ans, sol)
        # Test: Input is pandas.DataFrame without col parameter => pd.DataFrame
        ans = Calculator.returns(df)
        sol = pd.DataFrame(sol_matrix, index=df.index, columns=df.columns)
        self.assertEqual(ans, sol)

    def test_sharpe_ratio(self):
        array = np.array([1,1.5,3,4,4.3])
        array_2 = np.array([5,4.3,3,3.5,1])
        matrix = np.array([array, array_2]).T
        series = pd.Series(array)
        time_series = pd.TimeSeries(array_2)
        df = pd.DataFrame(matrix, columns=['c1', 'c2'])

        # Input is np.array of 1 dimmension => float
        ans = Calculator.sharpe_ratio(array)
        self.assertFloat(ans)
        self.assertAlmostEquals(ans, 2.38842, 5)
        # Input is np.array of 2 dimmensions => array
        ans = Calculator.sharpe_ratio(matrix)
        self.assertArray(ans)
        sol = np.array([2.38842482, -1.4708528])
        self.assertEqual(ans, sol, 5)
        # Input is pandas.Series => float
        ans = Calculator.sharpe_ratio(series)
        self.assertFloat(ans)
        self.assertAlmostEquals(ans, 2.38842, 5)
        # Input is pandas.TimeSeries => float
        ans = Calculator.sharpe_ratio(time_series)
        self.assertFloat(ans)
        self.assertAlmostEquals(ans, -1.4708528, 5)
        # Input is pandas.DataFrame with col parameter => float
        ans = Calculator.sharpe_ratio(df, col='c1')
        self.assertFloat(ans)
        self.assertAlmostEquals(ans, 2.38842, 5)
        # --
        ans = Calculator.sharpe_ratio(df, col='c2')
        self.assertFloat(ans)
        self.assertAlmostEqual(ans, -1.4708528, 5)
        # Input is pandas.DataFrame without col parameter => pd.Series
        ans = Calculator.sharpe_ratio(df)
        self.assertSeries(ans)
        sol = pd.Series([2.38842482, -1.4708528], index=['c1', 'c2'], name='Sharpe Ratios')
        self.assertEqual(ans, sol)


if __name__ == '__main__':
    suite = CalculatorTypesTest().suite()
    unittest.TextTestRunner(verbosity=2).run(suite)