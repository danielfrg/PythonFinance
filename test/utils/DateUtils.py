import unittest
import pandas as pd
from datetime import datetime

from finance.test import FinanceTest
from finance.utils import DateUtils

class DateUtilsTest(FinanceTest):

    def suite(self):
        suite = unittest.TestSuite()
        suite.addTest(DateUtilsTest('nyse_dates_basic'))
        suite.addTest(DateUtilsTest('nyse_dates_advanced'))
        suite.addTest(DateUtilsTest('nyse_dates_event'))
        suite.addTest(DateUtilsTest('nyse_add_and_substract'))
        return suite

    def nyse_dates_basic(self):
        '''
        Tests the dates without the lookBack and lookForward parameters
        '''
        # We assume this works: because sometime today is not and open day
        today = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
        dates = DateUtils.nyse_dates()
        today = DateUtils.search_closer_date(today, dates)
        today = dates[today]
        # End of assumssion
        
        # Test: Returns a list
        dates = DateUtils.nyse_dates()
        self.assertEquals(type(dates), list)
        # Test: Returns a pd.Series if requested
        dates = DateUtils.nyse_dates(series=True)
        self.assertEquals(type(dates), pd.Series)

        # Test: Default startdate is 2007-1-1
        dates = DateUtils.nyse_dates()
        ans = dates[0]
        self.assertEquals(ans, datetime(2007,1,3))
        # Test: Default enddate is today
        ans = dates[-1]
        self.assertEquals(ans, today)

        # Test: Values: start date after 2007-1-1
        start = datetime(2008, 1, 1)
        # Test: returns list
        dates = DateUtils.nyse_dates(start=start)
        self.assertEquals(type(dates), list)
        self.assertEquals(dates[0], datetime(2008, 1, 2))
        self.assertEquals(dates[-1], today)
        # Test: returns pd.Series
        dates = DateUtils.nyse_dates(start=start, series=True)
        self.assertEquals(type(dates), pd.Series)
        self.assertEquals(dates[0], datetime(2008, 1, 2))
        self.assertEquals(dates[-1], today)

        # Test: Values: start date before 2007-1-1
        start = datetime(1995, 1, 1)
        # Test: with list
        dates = DateUtils.nyse_dates(start=start)
        self.assertEquals(type(dates), list)
        self.assertEquals(dates[0], datetime(1995, 1, 3))
        self.assertEquals(dates[-1], today)
        # Test: with pd.Series
        dates = DateUtils.nyse_dates(start=start, series=True)
        self.assertEquals(type(dates), pd.Series)
        self.assertEquals(dates[0], datetime(1995, 1, 3))
        self.assertEquals(dates[-1], today)

        # Test: end date after 2007-1-1
        end = datetime(2009, 6, 6)
        dates = DateUtils.nyse_dates(end=end)
        self.assertEquals(type(dates), list)
        self.assertEquals(dates[0], datetime(2007, 1, 3))
        self.assertEquals(dates[-1], datetime(2009, 6, 5))

        # Test: end date before 2007-1-1
        end = datetime(2005, 6, 6)
        dates = DateUtils.nyse_dates(end=end)
        self.assertEquals(type(dates), list)
        self.assertEquals(dates[0], datetime(1962, 7, 5))
        self.assertEquals(dates[-1], datetime(2005, 6, 6))

        # Test: Values and lenght between 2 dates - No. 1
        start = datetime(2000, 1, 1)
        end = datetime(2002, 1, 1)
        # Test: with list
        dates = DateUtils.nyse_dates(start=start, end=end)
        self.assertEquals(type(dates), list)
        self.assertEquals(dates[0], datetime(2000, 1, 3))
        self.assertEquals(dates[-1], datetime(2001, 12, 31))
        self.assertEquals(len(dates), 500)
        # Test: with pd.Series
        dates = DateUtils.nyse_dates(start=start, end=end, series=True)
        self.assertEquals(type(dates), pd.Series)
        self.assertEquals(dates[0], datetime(2000, 1, 3))
        self.assertEquals(dates[-1], datetime(2001, 12, 31))
        self.assertEquals(len(dates), 500)

        # Test: Values and lenght between 2 dates - No. 2
        start = datetime(2009, 1, 1)
        end = datetime(2011, 1, 1)
        # Test: Lenght: Section - list
        dates = DateUtils.nyse_dates(start=start, end=end)
        self.assertEquals(type(dates), list)
        self.assertEquals(dates[0], datetime(2009, 1, 2))
        self.assertEquals(dates[-1], datetime(2010, 12, 31))
        self.assertEquals(len(dates), 504)
        # Test: Lenght: Section - pd.Series
        dates = DateUtils.nyse_dates(start=start, end=end, series=True)
        self.assertEquals(type(dates), pd.Series)
        self.assertEquals(dates[0], datetime(2009, 1, 2))
        self.assertEquals(dates[-1], datetime(2010, 12, 31))
        self.assertEquals(len(dates), 504)

    def nyse_dates_advanced(self):
        '''
        Tests the dates between two dates with the lookBack and lookForward parameters
        '''
        # Test: with lookbackDays without lookforwardDays
        start = datetime(2009, 1, 1)
        end = datetime(2011, 1, 1)
        dates = DateUtils.nyse_dates(start=start, end=end,
                        lookbackDays=10, lookforwardDays=0)
        self.assertEquals(dates[0], datetime(2008, 12, 17))
        self.assertEquals(dates[-1], datetime(2010, 12, 31))

        # Test: without lookbackDays with lookforwardDays
        start = datetime(2009, 1, 1)
        end = datetime(2011, 1, 1)
        dates = DateUtils.nyse_dates(start=start, end=end,
                        lookbackDays=0, lookforwardDays=10)
        self.assertEquals(dates[0], datetime(2009, 1, 2))
        self.assertEquals(dates[-1], datetime(2011, 1, 14))

        # Test: with lookbackDays with lookforwardDays
        start = datetime(2009, 1, 1)
        end = datetime(2011, 1, 1)
        dates = DateUtils.nyse_dates(start=start, end=end,
                        lookbackDays=10, lookforwardDays=10)
        self.assertEquals(dates[0], datetime(2008, 12, 17))
        self.assertEquals(dates[-1], datetime(2011, 1, 14))

    def nyse_dates_event(self):
        dates = DateUtils.nyse_dates_event(datetime(2009, 1, 5), 10, 10, 250)
        self.assertEquals(dates[0], datetime(2007, 12, 21))
        self.assertEquals(dates[-1], datetime(2009, 1, 20))
        self.assertEquals(len(dates), 271)

    def nyse_add_and_substract(self):
        ans = DateUtils.nyse_add(datetime(2009, 4, 13), 5)
        self.assertEquals(ans, datetime(2009, 4, 20))

        ans = DateUtils.nyse_substract(datetime(2009, 4, 13), 5)        
        self.assertEquals(ans, datetime(2009, 4, 3))

        ans = DateUtils.nyse_add(datetime(1990, 10, 1), 7)
        self.assertEquals(ans, datetime(1990, 10, 10))

        ans = DateUtils.nyse_substract(datetime(1990, 10, 1), 3)        
        self.assertEquals(ans, datetime(1990, 9, 26))

if __name__ == '__main__':
    suite = DateUtilsTest().suite()
    unittest.TextTestRunner(verbosity=2).run(suite)