import unittest
from datetime import datetime

from finance.utils import FileManager

class FileManagerTest(unittest.TestCase):

    def setUp1(self):
        self.file_manager = FileManager('./data')
        self.file_manager.empty_dir(delete=False)

    def suite(self):
        suite = unittest.TestSuite()
        suite.addTest(FileManagerTest('test_get_filenames'))
        return suite

    def test_get_filenames(self):
        '''
        Mainly tets the name of the files, more test on testExists()
        '''
        self.setUp1()
        symbols = ["AAPL","GLD","GOOG","SPY","XOM"]

        # Test: return empty list on missing file and downloadMissing=False
        start_date = datetime(2008, 1, 1)
        end_date = datetime(2009, 12, 31)
        ans = self.file_manager.get_filenames(symbols[0], start_date, end_date, downloadMissing=False)
        self.assertEqual(ans, [])

        # Test: return None on missing file and downloadMissing=False and ignoreMissing=False
        ans = self.file_manager.get_filenames(symbols[0], start_date, end_date, downloadMissing=False, ignoreMissing=False)
        self.assertEqual(ans, None)

        # Test: Download file and test name
        ans = self.file_manager.get_filenames(symbols[0], start_date, end_date, downloadMissing=True)
        self.assertEqual(ans, "AAPL_2008-1-1_2009-12-31.csv")

        # Test: Smaller start date: don't download un-necessary information
        start_date = datetime(2008, 6, 6) # Smaller
        end_date = datetime(2009, 12, 31)
        ans = self.file_manager.get_filenames(symbols[0], start_date, end_date, downloadMissing=True)
        self.assertEqual(ans, "AAPL_2008-1-1_2009-12-31.csv")

        # Test: Smaller end date: don't download un-necessary files
        start_date = datetime(2008, 1, 1)
        end_date = datetime(2009, 6, 6) # Smaller
        ans = self.file_manager.get_filenames(symbols[0], start_date, end_date, downloadMissing=True)
        self.assertEqual(ans, "AAPL_2008-1-1_2009-12-31.csv")

        # Test: Bigger start date: download another file
        start_date = datetime(2007, 1, 1) # Bigger
        end_date = datetime(2009, 6, 6)  # Smaller
        ans = self.file_manager.get_filenames(symbols[0], start_date, end_date, downloadMissing=True)
        self.assertEqual(ans, "AAPL_2007-1-1_2009-6-6.csv")

        # Test: Bigger end date: download another file
        start_date = datetime(2007, 1, 1) # Bigger
        end_date = datetime(2010, 6, 6) # Smaller
        ans = self.file_manager.get_filenames(symbols[0], start_date, end_date, downloadMissing=True)
        self.assertEqual(ans, "AAPL_2007-1-1_2010-6-6.csv")

        # Test: Download multiple files
        start_date = datetime(2005, 1, 1)
        end_date = datetime(2010, 1, 1)
        ans = self.file_manager.get_filenames(symbols, start_date, end_date, downloadMissing=True)
        sol = ["AAPL_2005-1-1_2010-1-1.csv", "GLD_2005-1-1_2010-1-1.csv",
                "GOOG_2005-1-1_2010-1-1.csv", "SPY_2005-1-1_2010-1-1.csv",
                "XOM_2005-1-1_2010-1-1.csv"]
        self.assertEqual(ans, sol)

        # Test: do not return missing filenames
        symbols = ["AAPL","FAKE1","GLD","FAKE1","GOOG","SPY","XOM","FAKE1"]
        ans = self.file_manager.get_filenames(symbols, start_date, end_date, downloadMissing=True)
        sol = ["AAPL_2005-1-1_2010-1-1.csv", "GLD_2005-1-1_2010-1-1.csv",
                "GOOG_2005-1-1_2010-1-1.csv", "SPY_2005-1-1_2010-1-1.csv",
                "XOM_2005-1-1_2010-1-1.csv"]
        self.assertEqual(ans, sol)

        # Test: Return missing filenames if requested
        symbols = ["AAPL","FAKE1","GLD","FAKE1","GOOG","SPY","XOM","FAKE1"]
        ans = self.file_manager.get_filenames(symbols, start_date, end_date, downloadMissing=True, ignoreMissing=False)
        sol = ["AAPL_2005-1-1_2010-1-1.csv", None, "GLD_2005-1-1_2010-1-1.csv",
                None, "GOOG_2005-1-1_2010-1-1.csv", "SPY_2005-1-1_2010-1-1.csv",
                "XOM_2005-1-1_2010-1-1.csv", None]
        self.assertEqual(ans, sol)

if __name__ == '__main__':
    suite = FileManagerTest().suite()
    unittest.TextTestRunner(verbosity=2).run(suite)

    FileManager('./data').empty_dir(delete=True)
