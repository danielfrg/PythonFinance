import os
import hashlib
import pandas as pd
from datetime import datetime
from finance.utils.FileManager import FileManager

class DataAccess(object):
    '''
    Class to manage the Access to the Data
    Features:
        1. Easy access to the data
        2. Download data from Yahoo! Finance
        3. Serialization of the data
    '''
    def __init__(self, dir_path='./data/'):
        self.set_dir(dir_path)

    def set_dir(self, dir_path):
        '''
        Initialize the FileManager
        Creates the directories
        Set global variables with absolute paths to the directories
        '''
        self.dir = os.path.realpath(dir_path) # Absolute Path
        self.cache_dir = os.path.join(self.dir, 'cached')
        self.file_manager = FileManager(dir_path)

        # Create paths if it doesn't exist
        if not (os.access(self.dir, os.F_OK)):
            os.makedirs(self.dir)
        if not (os.access(self.cache_dir, os.F_OK)):
            os.makedirs(self.cache_dir)

    def empty_dir(self, delete=True):
        '''
        Empty the directory of .csv files. Do not delete the cache files/folder
        Parameters:
            delete=True - True if want to delete the folder too
        '''
        self.file_manager.empty_dir(delete)

    def empty_cache(self, delete=True):
        '''
        Empty the directory of cached files. Do not delete the .csv files/folder
        Parameters:
            delete=True - True if want to delete the folder too
        '''
        list_files = os.listdir(self.cache_dir) # Get the list of files
        for f in list_files:
            try:
                os.remove(os.path.join(self.cache_dir, f))
            except:
                pass

        if delete:
            os.rmdir(self.cache_dir)

    def empty_dirs(self, delete=True):
        '''
        Delete both cached files and .csv files.
        Parameters:
            delete=True - True if want to delete the folders too
        '''
        self.empty_cache(delete)
        self.empty_dir(delete)

    def get_data(self, symbol_s, start_date, end_date, field_s, save=True, useCache=True,
                                downloadMissing=True):
        '''
        1. Checks if the data requeted has been previously cached:
            1.1 if it was saved, then load the cache version
            1.2 if not loads the data from the .csv files
                1.2.1 saves the cache version (optional)

        Args:
            symbols_s - symbol (str) or list of symbols
            start_date - datetime with the initial date
            end_date - datetime with the final date
            field_s - field (str) or list of fields
            save=True - True if want to save the cache version
            useCache=True - True if want to load a cached version, if available
            downloadMissing=True - True if want to download unavailable data

        Returns:
            pandas.DataFrame - with the data of the symbols and fields requested
                                index:
        '''
        # 0. Generate and string which represents the data requested
        filename_large = "%s_%s_%s_%s" % ('_'.join(symbol_s), start_date.strftime('%m-%d-%Y'),
                            end_date.strftime('%m-%d-%Y'), '-'.join(field_s))
        # 0. Generates hash key of the string to reduce filename length
        h = hashlib.md5()
        h.update(filename_large.encode('utf8'))
        filename = h.hexdigest() + ".data"
        # 1. Load the Data
        data = self.load(filename)
        if data is not None and useCache == True:
            # 1.1 Data was cached so return it
            return data
        else:
            # 1.2 Data was not cached before need to load the data from csv files
            df = self.get_data_from_files(symbol_s, start_date, end_date, field_s, downloadMissing)
            if save == True:
                # 1.2.1 Saves the cache version
                self.save(df, filename)
            return df

    def load(self, name):
        '''
        Checks for an existing file name and if exists returns the data saved
        '''
        f = os.path.join(self.cache_dir, name)
        if os.access(f, os.F_OK):
            return pd.load(f)
        else:
            return None

    def save(self, data, name):
        '''
        Save a serialized (pickle) version of the data to the cache directory
        '''
        f = os.path.join(self.cache_dir, name)
        data.save(f)

    def get_data_from_files(self, symbol_s, start_date, end_date, field_s, downloadMissing=True):
        '''
        Gets the data directly from the csv files

        Args:
            symbols_s - symbol (str) or list of symbols
            start_date - datetime with the initial date
            end_date - datetime with the final date
            field_s - field (str) or list of fields
            downloadMissing=True - True if want to download missing information from the internet

        Returs:
            pandas.DataFrame - with the data of the symbols and fields requested
                                index: DatetimeIndex
        '''
        # 0. If ask for only one symbols or field convert it to a list of one item
        if type(symbol_s) == str:
            symbol_s = [symbol_s]
        if type(field_s) == str:
            field_s = [field_s]

        # 1. We are going to create a pd.DataFrame from a dictionary of pd.Series
        data_dic = {}
        # 1.1 Save the Indexes of the data

        # 2. Get the file names with the information needed from the FileManager
        files = self.file_manager.get_data(symbol_s, start_date, end_date, downloadMissing)
        if type(files) == str:
            files = [files]

        for f, symbol in zip(files, symbol_s):
            # for each file in files and symbol in symbol_s
            n_data = pd.read_csv(os.path.join(self.dir, f))
            # Needs to convert the string to datetime so the index of the Series is DatetimeIndex
            n_data = n_data.set_index(pd.to_datetime(n_data['Date']))

            for field in field_s:
                # For each field in fields
                colname = ''
                if len(symbol_s) == 1 and len(field_s) == 1:
                    # Single symbol and Single field
                    colname = field
                elif len(symbol_s) > 1 and len(field_s) == 1:
                    # Multiple symbols and single fields
                    colname = symbol
                elif len(symbol_s) == 1 and len(field_s) > 1:
                    # Single symbol and Multiple fields
                    colname = field
                else:
                    # Multiple symbols and multiple fields
                    colname = "%s %s" % (symbol, field)
                # Adds the pd.Series to the dictionary
                data_dic[colname] = n_data[field]

        # 3. Create and return a pd.DataFrame from the dictionary of pd.Series
        df = pd.DataFrame(data_dic)
        df = df.sort() # Sort because Yahoo Finance data comes reverse
        return df.ix[start_date:end_date] # Slice by date to only return what is important

if __name__ == "__main__":
    da = DataAccess("./data")
    symbols = ["AAPL","GLD","GOOG","SPY","XOM"]
    start_date = datetime(2007, 6, 6)
    end_date = datetime(2009, 12, 31)
    fields = "Close"
    a = da.get_data('AAPL', start_date, end_date, fields, useCache=False)
    print(a)

    #da.empty_dirs(delete=True)

