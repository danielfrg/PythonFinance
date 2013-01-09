import unittest
import numpy as np
import pandas as pd
import numpy.testing as np_test
import pandas.util.testing as pd_test

import os, inspect
from finance.utils import DataAccess

class FinanceTest(unittest.TestCase):

    def setUpDataAccess(self, delete=False):
        self_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        DataAccess.path = os.path.join(self_dir, 'data')
        self.data_access = DataAccess()

        self.data_access.empty_cache(delete=delete)
        self.data_access.empty_dir(delete=delete)

    @staticmethod
    def delete_data():
        self_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        DataAccess.path = os.path.join(self_dir, 'data')
        data_access = DataAccess()
        data_access.empty_dirs()

    def assertEqual(self, ans, sol, digits=0):
        if type(ans) == np.ndarray and type(sol) == np.ndarray:
            self.assertArrayEqual(ans, sol, digits)
        elif type(ans) == pd.Series and type(sol) == pd.Series:
            self.assertSeriesEqual(ans, sol)
        elif type(ans) == pd.TimeSeries and type(sol) == pd.TimeSeries:
            self.assertSeriesEqual(ans, sol, digits)
        elif type(ans) == pd.DataFrame and type(sol) == pd.DataFrame:
            self.assertFrameEqual(ans, sol, digits)
        else:
            if digits == 0:
                super().assertEqual(ans, sol)
            else:
                super().assertAlmostEqual(ans, sol, digits)


    def assertFloat(self, obj):
        self.assertIs(type(obj), (np.float64))

    def assertArray(self, obj):
        self.assertIs(type(obj), np.ndarray)

    def assertArrayEqual(self, ans, sol, digits=0):
        self.assertArray(ans)
        self.assertArray(sol)
        if digits == 0:
            np_test.assert_array_equal(ans, sol)
        else:
            np_test.assert_array_almost_equal(ans, sol, digits)
    
    def assertSeries(self, obj):
        if type(obj) is pd.Series or type(obj) is pd.TimeSeries:
            return
        else:
            self.assertIs(type(obj), pd.Series)

    def assertSeriesEqual(self, ans, sol, digits=0):
        self.assertSeries(ans)
        self.assertSeries(sol)
        self.assertEquals(ans.name, sol.name)

        if digits == 0:
            pd_test.assert_series_equal(ans, sol, digits)
        else:
            np_test.assert_array_almost_equal(ans.values, sol.values, digits)

    def assertFrame(self, obj):
        self.assertIs(type(obj), pd.DataFrame)

    def assertFrameEqual(self, ans, sol, digits=0):
        self.assertFrame(ans)
        self.assertFrame(sol)
        self.assertEquals(ans.columns.name, sol.columns.name)

        if digits == 0:
            pd_test.assert_frame_equal(ans, sol)
        else:
            np_test.assert_array_almost_equal(ans.values, sol.values, digits)

