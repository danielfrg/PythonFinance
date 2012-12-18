# Test imports
import unittest

# General imports
from datetime import datetime
from finance.utils import FileManager

class FileManagerTest(unittest.TestCase):

    def setUp1(self):
        FileManager('./data').empty_dir()
        self.fm = FileManager('./data')

    def suite(self):
        suite = unittest.TestSuite()
        suite.addTest(FileManagerTest('test_get_data'))
        suite.addTest(FileManagerTest('test_exists'))
        return suite

    def test_get_data(self):
        '''
        Mainly tets the name of the files, more test for fm.get_data() on testExists()
        '''
        self.setUp1()

        # Test: return None on missing and downloadMissing=False
        symbols = ["AAPL","GLD","GOOG","SPY","XOM"]
        start_date = datetime(2008, 1, 1)
        end_date = datetime(2009, 12, 31)
        ans = self.fm.get_data(symbols[0], start_date, end_date, downloadMissing=False)
        self.assertEqual(ans, None)

        # Test: Download file and test name
        ans = self.fm.get_data(symbols[0], start_date, end_date, downloadMissing=True)
        self.assertEqual(ans, "AAPL_1-1-2008_12-31-2009.csv")

        # Test: smaller dates so gives the same file, dont download un-necessary files
        start_date = datetime(2008, 6, 6)
        end_date = datetime(2009, 12, 31)
        ans = self.fm.get_data(symbols[0], start_date, end_date, downloadMissing=True)
        self.assertEqual(ans, "AAPL_1-1-2008_12-31-2009.csv")

        start_date = datetime(2008, 1, 1)
        end_date = datetime(2009, 6, 6)
        ans = self.fm.get_data(symbols[0], start_date, end_date, downloadMissing=True)
        self.assertEqual(ans, "AAPL_1-1-2008_12-31-2009.csv")

        # Test: bigger dates, download another file
        start_date = datetime(2007, 1, 1) # Bigger
        end_date = datetime(2009, 6, 6) # Smaller
        ans = self.fm.get_data(symbols[0], start_date, end_date, downloadMissing=True)
        self.assertEqual(ans, "AAPL_1-1-2007_6-6-2009.csv")

        # Test: bigger dates, download another file
        start_date = datetime(2007, 1, 1) # Bigger
        end_date = datetime(2010, 6, 6) # Smaller
        ans = self.fm.get_data(symbols[0], start_date, end_date, downloadMissing=True)
        self.assertEqual(ans, "AAPL_1-1-2007_6-6-2010.csv")

        # Test: Download multiple files
        start_date = datetime(2005, 1, 1)
        end_date = datetime(2010, 1, 1)
        ans = self.fm.get_data(symbols, start_date, end_date, downloadMissing=True)
        sol = ["AAPL_1-1-2005_1-1-2010.csv", "GLD_1-1-2005_1-1-2010.csv",
                "GOOG_1-1-2005_1-1-2010.csv", "SPY_1-1-2005_1-1-2010.csv",
                "XOM_1-1-2005_1-1-2010.csv"]
        self.assertEqual(ans, sol)

    def test_exists(self):
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
    suite = FileManagerTest().suite()
    unittest.TextTestRunner(verbosity=2).run(suite)

    FileManager('./data').empty_dir(delete=True)
