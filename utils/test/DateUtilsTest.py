import unittest
from datetime import datetime
from finance.utils import DataAccess
from finance.utils import DateUtils

class DateUtilsTest(unittest.TestCase):

    def setUp1(self):
        pass
        #DataAccess('./data').empty_dirs()
        #self.da = DataAccess('./data')

    def suite(self):
        suite = unittest.TestSuite()
        suite.addTest(DateUtilsTest('get_nyse_dates'))
        suite.addTest(DateUtilsTest('get_nyse_dates_event'))
        return suite

    def get_nyse_dates(self):
        # Test: Returns a pd.Series
        dates = DateUtils.get_nyse_dates()
        self.assertNotEquals(type(dates), list)
        self.assertEquals(len(dates), 14728)

        # Test: Returns a list
        dates = DateUtils.get_nyse_dates(list=True)
        self.assertEquals(type(dates), list)
        self.assertEquals(len(dates), 14728)

    def get_nyse_dates_event(self):
        # Test: Returns a pd.Series
        dates = DateUtils.get_nyse_dates_event(datetime(2009, 1, 5), 100, 100)
        self.assertNotEquals(type(dates), list)
        self.assertEquals(len(dates), 201)
        self.assertEquals(dates[0], datetime(2008, 8, 12))
        self.assertEquals(dates[-1], datetime(2009, 5, 29))

        # Test: Returns a list
        dates = DateUtils.get_nyse_dates_event(datetime(2009, 1, 5), 50, 50, list=True)
        self.assertEquals(type(dates), list)
        self.assertEquals(len(dates), 101)




if __name__ == '__main__':
    suite = DateUtilsTest().suite()
    unittest.TextTestRunner(verbosity=2).run(suite)

    DataAccess('./data').empty_dirs(delete=True)