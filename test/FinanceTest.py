import unittest
import numpy as np
import pandas as pd
import numpy.testing as np_test
import pandas.util.testing as pd_test

from finance.utils import DataAccess

class FinanceTest(unittest.TestCase):

    def setUpEmptyDataAccess(self):
        DataAccess.path = 'data'
        self.data_access = DataAccess()
        self.data_access.empty_dirs(delete=False)

    @staticmethod
    def delete_data():
        DataAccess.path = 'data'
        DataAccess().empty_dirs()

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
        self.assertIs(type(obj), pd.Series)

    def assertSeriesEqual(self, ans, sol, testName=True):
        self.assertSeries(ans)
        self.assertSeries(sol)
        pd_test.assert_series_equal(ans, sol)
        if testName:
            self.assertEquals(ans.name, sol.name)

    def assertFrame(self, obj):
        self.assertIs(type(obj), pd.DataFrame)

    def assertFrameEqual(self, ans, sol, testName=True):
        self.assertFrame(ans)
        self.assertFrame(sol)
        pd_test.assert_frame_equal(ans, sol)
        if testName:
            self.assertEquals(ans.columns.name, sol.columns.name)

