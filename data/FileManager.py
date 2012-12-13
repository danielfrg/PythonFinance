import os
import sys
from datetime import datetime
import urllib.request
import urllib.parse

class FileManager(object):
    '''
    Class to manage the files from:
        - Yahoo Finance
    '''
    def __init__(self, dir_path='./data/'):
        self.set_dir(dir_path)

    def set_dir(self, dir_path):
        self.dir = os.path.realpath(dir_path) # Absolute Path

        #Create path if it doesn't exist
        if not (os.access(self.dir, os.F_OK)):
            os.makedirs(self.dir)

    def get_dir(self):
        return self.dir

    def empty_dir(self):
        list_files = os.listdir(self.dir) # Get the list of files
        for f in list_files:
            os.remove(os.path.join(self.dir, f))

    def get_data(self, symbol_s, start_date, end_date, downloadMissing=True):
        '''
        Returns file paths of the symbol(str)/symbols(list) who contains the
        information between the dates. If data is not available download the
        missing data (optional)

        Args:
            symbol_s - str for single - list of str for multiple

        Return:
            if single - str
            if multiple - list of str
        '''
        if type(symbol_s) == str:
            return self.get_data_single(symbol_s, start_date, end_date, downloadMissing)
        elif type(symbol_s) == list:
            return self.get_data_multiple(symbol_s, start_date, end_date, downloadMissing)

    def get_data_single(self, symbol, start_date, end_date, downloadMissing=True):
        list_files = os.listdir(self.dir) # Get the list of files

        for fi in list_files:
            # For each fi in files
            if fi.startswith(symbol):
                # Check the name of the stock
                # fi[:-4] removes the .csv and split to get each date
                fi_start_date = datetime.strptime(fi[:-4].split('_')[1], "%m-%d-%Y")
                fi_end_date = datetime.strptime(fi[:-4].split('_')[2], "%m-%d-%Y")
                # Check the dates of the file are greater or equal than the requested
                if fi_start_date <= start_date and fi_end_date >= end_date:
                    return fi

        # Saw al files and didnt found the information, so download it
        if downloadMissing:
            success = self.yahoo_download(symbol, start_date, end_date)
            if success:
                # If download was susccesfull returns (run again to get file path)
                return self.get_data_single(symbol, start_date, end_date, downloadMissing)
        return None

    def get_data_multiple(self, symbols, start_date, end_date, downloadMissing=True):
        ans = []
        for symbol in symbols:
            ans.append(self.get_data_single(symbol, start_date, end_date, downloadMissing))
        return ans

    def exists(self, symbol_s, start_date, end_date):
        '''
        Checks is a symbols or lists of symbols have the information between the
        specified dates

        Args:
            symbols can be an string or list of strings

        Returns:
            if single - boolean if information is available
            if multiple - list of booleans
        '''
        if type(symbol_s) == str:
            return not (self.get_data(symbol_s, start_date, end_date, False) == None)
        elif type(symbol_s) == list:
            d = self.get_data(symbol_s, start_date, end_date, False)
            return [ not (x == None) for x in d ]

    def yahoo_download(self, symbol, start_date, end_date):
        '''
        Download symbol information from Yahoo Finance

        Args:
            symbol
            start_date
            end_date

        Returns:
            boolean - True if was able to download, False otherwise
        '''
        try:
            params = urllib.parse.urlencode({
                                's': str(symbol),
                                'a': start_date.month - 1, 'b': start_date.day, 'c': start_date.year,
                                'd': end_date.month - 1, 'e': end_date.day, 'f': end_date.year
                            })

            webFile = urllib.request.urlopen("http://ichart.finance.yahoo.com/table.csv?%s" % params)
            filename = "%s_%d-%d-%d_%d-%d-%d.csv" % (symbol, start_date.month, start_date.day,
                        start_date.year, end_date.month, end_date.day, end_date.year)
            localFile = open( os.path.join(self.dir, filename), 'w')
            localFile.write(webFile.read().decode('utf-8'))
            webFile.close()
            localFile.close()
            return True
        except:
            #print(sys.exc_info()[1]) # TODO: logger
            return False

if __name__ == "__main__":
    fm = FileManager("../../data/")
    symbols = ["AAPL","GLD","GOOG","SPY","XOM", "FAKE1"]
    start_date = datetime(2008, 1, 1)
    end_date = datetime(2009, 12, 31)
    a = fm.get_data(symbols, start_date, end_date, downloadMissing=False)
    print (a)
