import os
import hashlib
import pandas as pd
from datetime import datetime
from finance.data.FileManager import FileManager

class DataAccess(object):
    def __init__(self, dir_path='./data/'):
        self.set_dir(dir_path)

    def set_dir(self, dir_path):
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
        list_files = os.listdir(self.dir) # Get the list of files
        for f in list_files:
            try:
                os.remove(os.path.join(self.dir, f))
            except:
                pass

    def empty_cache(self):
        list_files = os.listdir(self.cache_dir) # Get the list of files
        for f in list_files:
            os.remove(os.path.join(self.cache_dir, f))

    def empty_dirs(self):
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


        name = self.generate_filename(symbol_s, start_date, end_date, field_s)
        data = self.load(name)
        if data is not None and useCache == True:
            # Data was cached so return it
            return data
        else:
            # Data was not cached need to load the data from csv files
            df = self.get_data_file(symbol_s, start_date, end_date, field_s, downloadMissing)
            if save == True:
                name = self.generate_filename(symbol_s, start_date, end_date, field_s)
                self.save(df, name)
            return df

    def load(self, name):
        '''
        Checks for an existing file name and if exists load the data
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

    def generate_filename(self, symbol_s, start_date, end_date, field_s):
        '''
        Hash funcion used to compress the filename of the cached files
        '''
        string = "%s_%s_%s_%s" % ('_'.join(symbol_s), start_date.strftime('%m-%d-%Y'),
                            end_date.strftime('%m-%d-%Y'), '-'.join(field_s))
        h = hashlib.md5()
        h.update(string.encode('utf8'))
        filename = h.hexdigest() + ".data"
        return filename

    def get_data_file(self, symbol_s, start_date, end_date, field_s, downloadMissing=True):
        '''
        Gets the data directly from the csv files

        Args:
            symbols_s: symbol (str) or list of symbols
            field_s: field (str) or list of fields

        Returs:
            Pandas.DataFrame - with the information requested
        '''
        # If ask for only one symbols or field convert it to a lists
        if type(symbol_s) == str:
            symbol_s = [symbol_s]
        if type(field_s) == str:
            field_s = [field_s]

        # We are going to create a pd.DataFrame from a dictionary of pd.Series
        data_dic = {}
        # Get the file names with the info
        files = self.fm.get_data(symbol_s, start_date, end_date, downloadMissing)

        for f, symbol in zip(files, symbol_s):
            # for each file in files and symbol in symbol_s
            n_data = pd.read_csv(os.path.join(self.dir, f))
            n_data = n_data.set_index('Date') # Index of the DataFrame is the date

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
        return pd.DataFrame(data_dic)

if __name__ == "__main__":
    da = DataAccess("../../data")
    symbols = ["AAPL","GLD","GOOG","SPY","XOM"]
    start_date = datetime(2007, 6, 6)
    end_date = datetime(2009, 12, 31)
    fields = "Close"
    a = da.get_data(symbols, start_date, end_date, fields, useCache=False)
    print (a)

