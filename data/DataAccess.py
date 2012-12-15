import os
import hashlib
import pandas as pd
from datetime import datetime
from finance.data.FileManager import FileManager

class DataAccess(object):
    def __init__(self, dir_path='./data/'):
        self.set_dir(dir_path)

    def set_dir(self, dir_path):
        '''
        Create global class names and creates the directories for .csv
        files and cache files
        '''
        self.dir = os.path.realpath(dir_path) # Absolute Path
        self.cache_dir = os.path.join(self.dir, 'cached')
        self.fm = FileManager(dir_path)

        # Create paths if it doesn't exist
        if not (os.access(self.dir, os.F_OK)):
            os.makedirs(self.dir)
        if not (os.access(self.cache_dir, os.F_OK)):
            os.makedirs(self.cache_dir)

    def get_dir(self):
        return self.dir

    def empty_dir(self):
        '''
        Empty the directory of .CSV files, do not delete the cache files
        '''
        list_files = os.listdir(self.dir) # Get the list of files
        for f in list_files:
            try:
                os.remove(os.path.join(self.dir, f))
            except:
                pass

    def empty_cache(self):
        '''
        Empty the directory of cached files, do not delete the csv files
        '''
        list_files = os.listdir(self.cache_dir) # Get the list of files
        for f in list_files:
            os.remove(os.path.join(self.cache_dir, f))

    def empty_dirs(self):
        '''
        Empty both directories, cached files and csv files
        '''
        self.empty_cache()
        self.empty_dir()

    def get_data(self, symbol_s, start_date, end_date, field_s, save=True, useCache=True,
                                downloadMissing=True):
        '''
        Checks if the data requeted was previously been cached, if it was load
        the cache version, if not loads the data from the .csv files and saves
        the cache version (optional)

        Args:
            symbols_s - symbol (str) or list of symbols
            field_s - field (str) or list of fields
            save=True - True if want to save the cache version
            useCache=True - True if want to load a cached version, if available
            downloadMissing=True - True if want to download unavailable data
        '''
        # 1. Generate and string which represents the data requested
        filename_large = "%s_%s_%s_%s" % ('_'.join(symbol_s), start_date.strftime('%m-%d-%Y'),
                            end_date.strftime('%m-%d-%Y'), '-'.join(field_s))
        # 2. Generates hash key of the string to reduce filename
        h = hashlib.md5()
        h.update(filename_large.encode('utf8'))
        filename = h.hexdigest() + ".data"
        # 3. Load the Data
        data = self.load(filename)
        if data is not None and useCache == True:
            # 4. Data was cached so return it
            return data
        else:
            # 4. Data was not cached need to load the data from csv files
            df = self.get_data_file(symbol_s, start_date, end_date, field_s, downloadMissing)
            if save == True:
                self.save(df, filename)
            return df

    def load(self, name):
        '''
        Checks for an existing file name and if exists loads the cache version
        '''
        f = os.path.join(self.cache_dir, name)
        if os.access(f, os.F_OK):
            return pd.load(f)
        else:
            return None

    def save(self, data, name):
        '''
        Save a pickle serialized version of the data
        '''
        f = os.path.join(self.cache_dir, name)
        data.save(f)

    def get_data_file(self, symbol_s, start_date, end_date, field_s, downloadMissing=True):
        '''
        Gets the data directly from the csv files

        Args:
            symbols_s: symbol (str) or list of symbols
            field_s: field (str) or list of fields

        Returs:
            Pandas.DataFrame - with the information requested
        '''
        # 0. If ask for only one symbols or field convert it to a lists
        if type(symbol_s) == str:
            symbol_s = [symbol_s]
        if type(field_s) == str:
            field_s = [field_s]

        # 1. We are going to create a pd.DataFrame from a dictionary of pd.Series
        data_dic = {}
        # 1.1 Save the Indexes of the data
        indexes = None
        # 2. Get the file names with the info
        files = self.fm.get_data(symbol_s, start_date, end_date, downloadMissing)
        n_data = None # New Data for the iterations

        for f, symbol in zip(files, symbol_s):
            # for each file in files and symbol in symbol_s
            n_data = pd.read_csv(os.path.join(self.dir, f))
            # Needs to convert the string to datetime so the index of the DataFrame is DatetimeIndex
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
                    colname = "%s_%s" % (symbol, field)

                data_dic[colname] = n_data[field]

        # Return the pd.DataFrame from the dictionary of pd.Series
        df = pd.DataFrame(data_dic)
        df = df.sort() # Sort because Yahoo Finance data comes reverse
        return df.ix[start_date:end_date] # Slice by date

if __name__ == "__main__":
    da = DataAccess("../../data")
    symbols = ["AAPL","GLD","GOOG","SPY","XOM"]
    start_date = datetime(2007, 6, 6)
    end_date = datetime(2009, 12, 31)
    fields = "Close"
    a = da.get_data(symbols, start_date, end_date, fields, useCache=False)
    print(a)

