# General imports
from datetime import datetime
from finance.data.FileManager import FileManager

# Test imports
import os
import unittest

class TestFileManager(unittest.TestCase):

    def setUp1(self):
        self.fm = FileManager('./data')
        self.fm.emptyDir()

    def testGetData(self):
        '''
        Mainly tets the name of the files, more test for fm.get_data() on testExists()
        '''
        self.setUp1()

        # Test return None on missing
        symbols = ["AAPL","GLD","GOOG","SPY","XOM"]
        start_date = datetime(2008, 1, 1)
        end_date = datetime(2009, 12, 31)
        ans = self.fm.get_data(symbols[0], start_date, end_date, downloadMissing=False)
        self.assertEqual(ans, None)

        # Test name on non-missing
        ans = self.fm.get_data(symbols[0], start_date, end_date, downloadMissing=True)
        self.assertEqual(ans, "AAPL_1-1-2008_12-31-2009.csv")

        # Test smaller dates gives the same file, dont download un-necessary files
        start_date = datetime(2008, 6, 6)
        end_date = datetime(2009, 12, 31)
        ans = self.fm.get_data(symbols[0], start_date, end_date, downloadMissing=True)
        self.assertEqual(ans, "AAPL_1-1-2008_12-31-2009.csv")

        start_date = datetime(2008, 1, 1)
        end_date = datetime(2009, 6, 6)
        ans = self.fm.get_data(symbols[0], start_date, end_date, downloadMissing=True)
        self.assertEqual(ans, "AAPL_1-1-2008_12-31-2009.csv")

        # Test bigger dates, download necessary files
        start_date = datetime(2007, 1, 1) # Bigger
        end_date = datetime(2009, 6, 6) # Smaller
        ans = self.fm.get_data(symbols[0], start_date, end_date, downloadMissing=True)
        self.assertEqual(ans, "AAPL_1-1-2007_6-6-2009.csv")

    def testExists(self):
        '''
        Since fm.exists() calls fm.get_data() tests works for it too
        '''
        self.setUp1()

        # Test without downloadMissing
        symbols = ["AAPL","GLD","GOOG","SPY","XOM"]
        start_date = datetime(2008, 1, 1)
        end_date = datetime(2009, 12, 31)
        # Single test
        ans = self.fm.exists(symbols[0], start_date, end_date)
        self.assertEqual(ans, False)
        # Multiple Test
        ans = self.fm.exists(symbols, start_date, end_date)
        self.assertEqual(ans, [False, False, False, False, False])

        # Test downloading
        symbols = ["AAPL","GLD","GOOG","SPY","XOM"]
        start_date = datetime(2008, 1, 1)
        end_date = datetime(2009, 12, 31)
        self.fm.get_data(symbols[0], start_date, end_date, downloadMissing=True)
        ans = self.fm.exists(symbols[0], start_date, end_date)
        self.assertEqual(ans, True)
        # Already download first, now download all but last
        self.fm.get_data(symbols[1:4], start_date, end_date, downloadMissing=True)
        ans = self.fm.exists(symbols[1:4], start_date, end_date)
        self.assertEqual(ans, [True, True, True])
        # Last should be missing
        ans = self.fm.exists(symbols[4], start_date, end_date)
        self.assertEqual(ans, False)
        # Download Last so shouldnt be missing
        self.fm.get_data(symbols[4], start_date, end_date, downloadMissing=True)
        ans = self.fm.exists(symbols[4], start_date, end_date)
        self.assertEqual(ans, True)

if __name__ == '__main__':
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFileManager)
    unittest.TextTestRunner(verbosity=2).run(suite)
