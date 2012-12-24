import unittest
from datetime import datetime
from finance.utils import FileManager

class FileManagerTest(unittest.TestCase):

    def setUp1(self):
        FileManager('./data').empty_dir()
        self.fm = FileManager('./data')

    def suite(self):
        suite = unittest.TestSuite()
        suite.addTest(FileManagerTest('test_get_data'))
        return suite

    def test_get_data(self):
        '''
        Mainly tets the name of the files, more test on testExists()
        '''
        self.setUp1()

        # Test: return None on missing file with downloadMissing=False
        symbols = ["AAPL","GLD","GOOG","SPY","XOM"]
        start_date = datetime(2008, 1, 1)
        end_date = datetime(2009, 12, 31)
        ans = self.fm.get_data(symbols[0], start_date, end_date, downloadMissing=False)
        self.assertEqual(ans, None)

        # Test: Download file and test name
        ans = self.fm.get_data(symbols[0], start_date, end_date, downloadMissing=True)
        self.assertEqual(ans, "AAPL_2008-1-1_2009-12-31.csv")

        # Test: smaller dates so gives the same file: dont download un-necessary files
        start_date = datetime(2008, 6, 6) # Smaller
        end_date = datetime(2009, 12, 31)
        ans = self.fm.get_data(symbols[0], start_date, end_date, downloadMissing=True)
        self.assertEqual(ans, "AAPL_2008-1-1_2009-12-31.csv")

        # Test: smaller dates so gives the same file: dont download un-necessary files
        start_date = datetime(2008, 1, 1)
        end_date = datetime(2009, 6, 6) # Smaller
        ans = self.fm.get_data(symbols[0], start_date, end_date, downloadMissing=True)
        self.assertEqual(ans, "AAPL_2008-1-1_2009-12-31.csv")

        # Test: bigger dates, download another file
        start_date = datetime(2007, 1, 1) # Bigger
        end_date = datetime(2009, 6, 6)  # Smaller
        ans = self.fm.get_data(symbols[0], start_date, end_date, downloadMissing=True)
        self.assertEqual(ans, "AAPL_2007-1-1_2009-6-6.csv")

        # Test: bigger dates, download another file
        start_date = datetime(2007, 1, 1) # Bigger
        end_date = datetime(2010, 6, 6) # Smaller
        ans = self.fm.get_data(symbols[0], start_date, end_date, downloadMissing=True)
        self.assertEqual(ans, "AAPL_2007-1-1_2010-6-6.csv")

        # Test: Download multiple files
        start_date = datetime(2005, 1, 1)
        end_date = datetime(2010, 1, 1)
        ans = self.fm.get_data(symbols, start_date, end_date, downloadMissing=True)
        sol = ["AAPL_2005-1-1_2010-1-1.csv", "GLD_2005-1-1_2010-1-1.csv",
                "GOOG_2005-1-1_2010-1-1.csv", "SPY_2005-1-1_2010-1-1.csv",
                "XOM_2005-1-1_2010-1-1.csv"]
        self.assertEqual(ans, sol)

if __name__ == '__main__':
    suite = FileManagerTest().suite()
    unittest.TextTestRunner(verbosity=2).run(suite)

    FileManager('./data').empty_dir(delete=True)
