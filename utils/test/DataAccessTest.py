import unittest
from datetime import datetime

from finance.utils import DataAccess

class DataAccessTest(unittest.TestCase):

    def setUp1(self):
        DataAccess('./data').empty_dirs()
        self.da = DataAccess('./data')

    def suite(self):
        suite = unittest.TestSuite()
        suite.addTest(DataAccessTest('test_get_data'))
        suite.addTest(DataAccessTest('test_save_load_custom_name'))
        return suite

    def test_get_data(self):
        '''
        Tests the length of row and columns and their names

        Note 1: File downloads are managed by finance.utils.FileManager
                Test for that on FileManagerTest.py
        Note 2: Other tests were done on the benchmark
        '''
        self.setUp1()

        start_date = datetime(2008, 1, 1)
        end_date = datetime(2009, 12, 31)

        # Single symbol, single field
        symbols = "AAPL"
        field_s = "Close"
        df = self.da.get_data(symbols, start_date, end_date, field_s)
        self.assertEqual(len(df), 505)
        self.assertEqual(len(df.columns), 1)
        names = [field_s]
        self.assertEqual(list(df.columns), names)

        # Multiple symbols, single field
        symbols = ["AAPL","GLD","GOOG","SPY","XOM"]
        field_s = "Close"
        df = self.da.get_data(symbols, start_date, end_date, field_s)
        self.assertEqual(len(df), 505)
        self.assertEqual(len(df.columns), 5)
        names = symbols
        self.assertEqual(list(df.columns), names)

        # Single symbol, multiple fields
        symbols = "AAPL"
        field_s = ["Close", "Volume"]
        df = self.da.get_data(symbols, start_date, end_date, field_s)
        self.assertEqual(len(df), 505)
        self.assertEqual(len(df.columns), 2)
        names = ['Close', 'Volume']
        self.assertEqual(list(df.columns), names)

        # Multiple symbol, multiple fields
        symbols = ["AAPL","GLD","GOOG","SPY","XOM"]
        field_s = ["Close", "Volume"]
        df = self.da.get_data(symbols, start_date, end_date, field_s)
        self.assertEqual(len(df), 505)
        self.assertEqual(len(df.columns), 10)
        names = ['AAPL Close', 'AAPL Volume', 'GLD Close', 'GLD Volume', 'GOOG Close',
                    'GOOG Volume', 'SPY Close', 'SPY Volume', 'XOM Close', 'XOM Volume']
        self.assertEqual(list(df.columns), names)

    def test_save_load_custom_name(self):
        self.setUp1()

        symbols = ["AAPL", "GLD", "GOOG", "SPY", "XOM"]
        start_date = datetime(2008, 1, 1)
        end_date = datetime(2009, 12, 31)
        fields = "Close"

        close = self.da.get_data(symbols, start_date, end_date, fields, save=False)
        self.da.save(close, "customName", extension='.custom')

        close_loaded = self.da.load("customName", extension='.custom')

        self.assertEqual(list(close.columns), list(close_loaded.columns))
        self.assertEqual(len(close), len(close_loaded))


def benchmark():
    from time import clock, time
    da = DataAccess('./data')
    da.empty_dirs(delete=False)

    print ('Directory empty: Download and save 5 stocks')
    t1, t2 = clock(), time()
    symbols = ["AAPL","GLD","GOOG","SPY","XOM"]
    start_date = datetime(2008, 1, 1)
    end_date = datetime(2009, 12, 31)
    field_s = "Close"
    da.get_data(symbols, start_date, end_date, field_s)
    t1_f, t2_f = clock(), time()
    print ("   ", t1_f - t1, t2_f - t2)

    print ('Load 5 stocks from .csv')
    t1, t2 = clock(), time()
    symbols = ["AAPL","GLD","GOOG","SPY","XOM"]
    start_date = datetime(2008, 1, 1)
    end_date = datetime(2009, 12, 31)
    field_s = "Close"
    da.get_data(symbols, start_date, end_date, field_s, useCache=False)
    t1_f, t2_f = clock(), time()
    print ("   ", t1_f - t1, t2_f - t2)

    print ('Load 5 stocks from serialized')
    t1, t2 = clock(), time()
    symbols = ["AAPL","GLD","GOOG","SPY","XOM"]
    start_date = datetime(2008, 1, 1)
    end_date = datetime(2009, 12, 31)
    field_s = "Close"
    da.get_data(symbols, start_date, end_date, field_s, useCache=True)
    t1_f, t2_f = clock(), time()
    print ("   ", t1_f - t1, t2_f - t2)

if __name__ == '__main__':
    suite = DataAccessTest().suite()
    unittest.TextTestRunner(verbosity=2).run(suite)

    benchmark()

    DataAccess('./data').empty_dirs(delete=True)
