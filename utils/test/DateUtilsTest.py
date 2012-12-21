import unittest
import pandas as pd
from datetime import datetime
from finance.utils import DataAccess
from finance.utils import DateUtils

class DateUtilsTest(unittest.TestCase):

    def setUp1(self):
        DataAccess('./data').empty_dirs()
        self.da = DataAccess('./data')

    def suite(self):
        suite = unittest.TestSuite()
        suite.addTest(DateUtilsTest('nyse_dates_basic'))
        suite.addTest(DateUtilsTest('nyse_dates_advanced'))
        suite.addTest(DateUtilsTest('nyse_dates_event'))
        return suite

    def nyse_dates_basic(self):
        '''
        Tests the dates between two dates without lookBack and lookForward
        For each test checks:
            1. type returned
            2. lenght of arrays
            3. initial and final dates returned
        List of tets:
            1. Ask for all dates
            2. Ask for dates with start date
            2. Ask for dates with end date
            2. Ask for dates between two dates
        '''
        # Test: Lenght: Complete - list
        dates = DateUtils.nyse_dates(list=True)
        self.assertEquals(type(dates), list)
        self.assertEquals(len(dates), 14728)
        # Test: Lenght: Complete - pd.Series
        dates = DateUtils.nyse_dates()
        self.assertEquals(type(dates), pd.TimeSeries)
        self.assertEquals(len(dates), 14728)

        # Test: Lenght: start date only
        start = datetime(2000, 1, 1)
        # Test: Lenght: Section - list
        dates = DateUtils.nyse_dates(start=start, list=True)
        self.assertEquals(type(dates), list)
        self.assertEquals(dates[0], datetime(2000, 1, 3))
        self.assertEquals(dates[-1], datetime(2020, 12, 31))
        self.assertEquals(len(dates), 5286 + 1)
        # Test: Lenght: Section - pd.Series
        dates = DateUtils.nyse_dates(start=start)
        self.assertEquals(type(dates), pd.TimeSeries)
        self.assertEquals(dates[0], datetime(2000, 1, 3))
        self.assertEquals(dates[-1], datetime(2020, 12, 31))
        self.assertEquals(len(dates), 5286 + 1)

        # Test: Lenght: end date only
        end = datetime(2002, 1, 1)
        # Test: Lenght: Section - list
        dates = DateUtils.nyse_dates(end=end, list=True)
        self.assertEquals(type(dates), list)
        self.assertEquals(dates[0], datetime(1962, 7, 5))
        self.assertEquals(dates[-1], datetime(2001, 12, 31))
        self.assertEquals(len(dates), 9941)
        # Test: Lenght: Section - pd.Series
        dates = DateUtils.nyse_dates(end=end)
        self.assertEquals(type(dates), pd.TimeSeries)
        self.assertEquals(dates[0], datetime(1962, 7, 5))
        self.assertEquals(dates[-1], datetime(2001, 12, 31))
        self.assertEquals(len(dates), 9941)

         # Test: Lenght: Section
        start = datetime(2009, 1, 1)
        end = datetime(2011, 1, 1)
        # Test: Lenght: Section - list
        dates = DateUtils.nyse_dates(start=start, end=end, list=True)
        self.assertEquals(type(dates), list)
        self.assertEquals(dates[0], datetime(2009, 1, 2))
        self.assertEquals(dates[-1], datetime(2010, 12, 31))
        self.assertEquals(len(dates), 504)
        # Test: Lenght: Section - pd.Series
        dates = DateUtils.nyse_dates(start=start, end=end)
        self.assertEquals(type(dates), pd.TimeSeries)
        self.assertEquals(dates[0], datetime(2009, 1, 2))
        self.assertEquals(dates[-1], datetime(2010, 12, 31))
        self.assertEquals(len(dates), 504)

    def nyse_dates_advanced(self):
        '''
        Tests the dates between two dates with lookBack and lookForward
        For each test checks:
            1. initial and final dates returned
            Note: Do not test type of data returned only values
        List of Tests:
            1. with lookbackDays without lookforwardDays
            2. without lookbackDays with lookforwardDays
            3. with lookbackDays with lookforwardDays
        '''
        # Test: with lookbackDays without lookforwardDays
        start = datetime(2009, 1, 1)
        end = datetime(2011, 1, 1)
        dates = DateUtils.nyse_dates(start=start, end=end,
                        lookbackDays=10, lookforwardDays=0, list=True)
        self.assertEquals(dates[0], datetime(2008, 12, 17))
        self.assertEquals(dates[-1], datetime(2010, 12, 31))

        # Test: without lookbackDays with lookforwardDays
        start = datetime(2009, 1, 1)
        end = datetime(2011, 1, 1)
        dates = DateUtils.nyse_dates(start=start, end=end,
                        lookbackDays=0, lookforwardDays=10, list=True)
        self.assertEquals(dates[0], datetime(2009, 1, 2))
        self.assertEquals(dates[-1], datetime(2011, 1, 14))

        # Test: with lookbackDays with lookforwardDays
        start = datetime(2009, 1, 1)
        end = datetime(2011, 1, 1)
        dates = DateUtils.nyse_dates(start=start, end=end,
                        lookbackDays=10, lookforwardDays=10, list=True)
        self.assertEquals(dates[0], datetime(2008, 12, 17))
        self.assertEquals(dates[-1], datetime(2011, 1, 14))

    def nyse_dates_event(self):
        '''
        '''
        dates = DateUtils.nyse_dates_event(datetime(2009, 1, 5), 100, 100)
        self.assertEquals(dates[0], datetime(2008, 8, 12))
        self.assertEquals(dates[-1], datetime(2009, 5, 29))
        self.assertEquals(len(dates), 201)

def benchmark_get_dates():
    from time import clock, time
    t1, t2 = clock(), time()
    DateUtils.nyse_dates(list=True, useCache=False)
    t1_f, t2_f = clock(), time()
    print("Load from file:", t1_f - t1, t2_f - t2)

    t1, t2 = clock(), time()
    DateUtils.nyse_dates(list=True)
    t1_f, t2_f = clock(), time()
    print ("Load from cache:", t1_f - t1, t2_f - t2)

if __name__ == '__main__':
    suite = DateUtilsTest().suite()
    unittest.TextTestRunner(verbosity=2).run(suite)

    #benchmark_get_dates()

    DataAccess('./data').empty_dirs(delete=True)
