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
        1. Set global variables with absolute paths to the directories
        2. Creates the directories

        Parameters
        ----------
            dir_path: str
        '''
        self.dir = os.path.realpath(dir_path) # Absolute Path

        #Create path if it doesn't exist
        if not (os.access(self.dir, os.F_OK)):
            os.makedirs(self.dir)

    def empty_dir(self, delete=True):
        '''
        Empty the directory of files

        Parameters
        ----------
            delete: boolean, True if want to delete the folder too
        '''
        list_files = os.listdir(self.dir) # Get the list of files
        for f in list_files:
            try:
                os.remove(os.path.join(self.dir, f))
            except:
                pass

        if delete:
            os.rmdir(self.dir)

    def get_filenames(self, symbol_s, start_date, end_date, downloadMissing=True, ignoreMissing=True):
        '''
        Returns a list with the file paths of the symbols
        which contains the information between the specified dates.
        Optional: If data is not available download the missing data

        Parameters
        ----------
            symbol_s: str for single - list of str for multiple
            start_date: datetime, with the initial date
            end_date: datetime, with the final date
            downloadMissing: boolean, True if want to download missing data

        Returns
        -------
            if single - str with the relative path to the file with the information
            if multiple - list of str with relative paths
        '''
        # 0. If only asks for one symbols convert it to a list
        if type(symbol_s) == str:
            symbols = [symbol_s]
        elif type(symbol_s) == list:
            symbols = symbol_s

        # 1. Get the list of files available
        list_files = [f for f in os.listdir(self.dir) if os.path.isfile(os.path.join(self.dir,f))]
        ans = []

        # For symbol in symbols and for each file_name in files
        for symbol in symbols:
            f = None
            for file_name in list_files:
                # Check the name of the stock
                if file_name.startswith(symbol):
                    # Check if the dates of the file are greater or equal than the requested
                    # Note: split to get each date and file_name[:-4] to remove the .csv
                    fi_start_date = datetime.strptime(file_name[:-4].split('_')[1], "%Y-%m-%d")
                    fi_end_date = datetime.strptime(file_name[:-4].split('_')[2], "%Y-%m-%d")
                    if fi_start_date <= start_date and fi_end_date >= end_date:
                        f = file_name

            if f is None and downloadMissing:
                success = self.yahoo_download(symbol, start_date, end_date)
                if success:
                    # If download was susccesfull add the path to the new file
                    f = "%s_%d-%d-%d_%d-%d-%d.csv" % (symbol, start_date.year, start_date.month,
                        start_date.day, end_date.year, end_date.month, end_date.day)
            
            if ignoreMissing == False:
                ans.append(f)
            else:
                if f is not None:
                    ans.append(f)


        if type(symbol_s) == str:
            return ans[0]
        else:
            return ans

    def yahoo_download(self, symbol, start_date, end_date):
        '''
        Downloads and saves the equitiy information from Yahoo! Finance between
        the specified dates.
        Saves the csv file with the name: SYMBOL_start_date_end_date.csv
            e.g: AAPL_2009-1-1_2010-1-1.csv

        Parameters
        ----------
            symbol: str
            start_date: datetime
            end_date: datetime

        Returns
        -------
            boolean: True if was able to download the symbol, False otherwise
        '''
        try:
            params = urllib.parse.urlencode({
                                's': str(symbol),
                                'a': start_date.month - 1, 'b': start_date.day, 'c': start_date.year,
                                'd': end_date.month - 1, 'e': end_date.day, 'f': end_date.year
                            })
            webFile = urllib.request.urlopen("http://ichart.finance.yahoo.com/table.csv?%s" % params)
            filename = "%s_%d-%d-%d_%d-%d-%d.csv" % (symbol, start_date.year, start_date.month,
                        start_date.day, end_date.year, end_date.month, end_date.day)
            localFile = open( os.path.join(self.dir, filename), 'w')
            localFile.write(webFile.read().decode('utf-8'))
            webFile.close()
            localFile.close()
            return True
        except:
            print(symbol, sys.exc_info()[1])
            return False