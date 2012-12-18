import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime

class FileManager(object):
    '''
    Class to manage the files from:
        - Yahoo Finance
    '''
    def __init__(self, dir_path='./data/'):
        self.set_dir(dir_path)

    def set_dir(self, dir_path):
        '''
        Creates the directories
        Set global variables with absolute paths to the directories
        '''
        self.dir = os.path.realpath(dir_path) # Absolute Path

        #Create path if it doesn't exist
        if not (os.access(self.dir, os.F_OK)):
            os.makedirs(self.dir)

    def empty_dir(self, delete=True):
        '''
        Empty the directory of files
        Parameters:
            delete=True - True if want to delete the folder too
        '''
        list_files = os.listdir(self.dir) # Get the list of files
        for f in list_files:
            try:
                os.remove(os.path.join(self.dir, f))
            except:
                pass

        if delete:
            os.rmdir(self.dir)

    def get_data(self, symbol_s, start_date, end_date, downloadMissing=True):
        '''
        Returns file paths of the symbol(str)/symbols(list) which contains the
        information between the dates. If data is not available download the
        missing data (optional)

        Args:
            symbol_s - str for single - list of str for multiple
            start_date - datetime with the initial date
            end_date - datetime with the final date

        Return:
            if single - str with the relative path to the file with the information
            if multiple - list of str with absolute paths
        '''
        # 0. If only asks for one symbols convert it to a list
        if type(symbol_s) == str:
            symbol_s = [symbol_s]

        # 1. Get the list of files
        list_files = os.listdir(self.dir)
        ans = []

        # For symbol in symbols and for each file_name in files
        for symbol in symbol_s:
            f = None
            for file_name in list_files:
                # Check the name of the stock
                if file_name.startswith(symbol):
                    # Check if the dates of the file are greater or equal than the requested
                    # Note: split to get each date and file_name[:-4] to remove the .csv
                    fi_start_date = datetime.strptime(file_name[:-4].split('_')[1], "%m-%d-%Y")
                    fi_end_date = datetime.strptime(file_name[:-4].split('_')[2], "%m-%d-%Y")
                    if fi_start_date <= start_date and fi_end_date >= end_date:
                        f = file_name

            if f is None and downloadMissing:
                success = self.yahoo_download(symbol, start_date, end_date)
                if success:
                    # If download was susccesfull add the path to the new file
                    f = "%s_%d-%d-%d_%d-%d-%d.csv" % (symbol, start_date.month, start_date.day,
                        start_date.year, end_date.month, end_date.day, end_date.year)
            ans.append(f)

        if len(ans) == 1:
            return ans[0]
        else:
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
            return [not (x == None) for x in d ]

    def yahoo_download(self, symbol, start_date, end_date):
        '''
        Downloads ans saves the symbol information between the specified dates from Yahoo Finance
        Saves the csv file with the name: SYMBOL_start_date_end_date.csv
             e.g: AAPL_2009-1-1_2010-1-1.csv
        Args:
            symbol
            start_date
            end_date

        Returns:
            boolean - True if was able to download all the symbols, False otherwise
        TODO: logger with the erros
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
            # TODO: logger
            print(sys.exc_info()[1])
            return False

if __name__ == "__main__":
    fm = FileManager("./data/")
    symbols = ["AAPL","GLD","GOOG","SPY","XOM", "FAKE1"]
    start_date = datetime(2008, 1, 1)
    end_date = datetime(2009, 12, 31)
    a = fm.get_data(symbols, start_date, end_date, downloadMissing=True)
    print (a)
    fm.empty_dir()
