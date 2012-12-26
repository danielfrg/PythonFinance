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
        2. Serialization of data
    '''
    def __init__(self, dir_path='./data/'):
        self.set_dir(dir_path)

    def set_dir(self, dir_path):
        '''
        Initialize the FileManager
        Creates the directories
        Set global variables with absolute paths to the directories

        Parameters
        ----------
            dir_path: str
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

        Parameters
        ----------
            delete:boolean, True if want to delete the folder too
        '''
        self.file_manager.empty_dir(delete)

    def empty_cache(self, delete=True):
        '''
        Empty the directory of cached files. Do not delete the .csv files/folder

        Parameters
        ----------
            delete: boolean, True if want to delete the folder too
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

        Parameters
        ----------
            delete:booelan, True if want to delete the folders too
        '''
        self.empty_cache(delete)
        self.empty_dir(delete)

    def save(self, data, name, extension='.data'):
        '''
        Saves a serialized (pickle) version of the data to the cache directory

        Parameters
        ----------
            data: object
            name: str, identifier of the data
            extension: str, extension of the filename
        '''
        h = hashlib.md5()
        h.update(name.encode('utf8'))
        filename = h.hexdigest() + extension

        f = os.path.join(self.cache_dir, filename)
        data.save(f)

    def load(self, name, extension='.data'):
        '''
        Checks for an existing file name and if exists returns the data saved

        Parameters
        ----------
            name: str, identifier of the data
            extension: str, extension of the filename

        Returns
        -------
            data: object, usually pandas.DataFrame. None if file is not
                    available
        '''
        h = hashlib.md5()
        h.update(name.encode('utf8'))
        filename = h.hexdigest() + extension

        f = os.path.join(self.cache_dir, filename)
        if os.access(f, os.F_OK):
            return pd.load(f)
        else:
            return None

    def generate_filename(self, symbols, start_date, end_date, field_s):
        '''
        Returns an unique filename identifier of a list of symbols and between dates
        '''
        filename_large = "%s_%s_%s_%s" % ('_'.join(symbols),
                                            start_date.strftime('%m-%d-%Y'),
                                            end_date.strftime('%m-%d-%Y'),
                                            '-'.join(field_s))
        h = hashlib.md5()
        h.update(filename_large.encode('utf8'))
        return h.hexdigest()

    def get_data(self, symbol_s, start_date, end_date, field_s, save=True, useCache=True,
                                downloadMissing=True):
        '''
        Returns a pandas DataFrame with the data of the symbol/symbols and field
        fields between the specified dates.
        If cache version is available load it (optional) if not available
        load the data from the csv files.
        Optional: Saves a serialized version of the data
        Optional: If data is not available download the missing data

        Parameters
        ----------
            symbols_s: str or list of str
            start_date: datetime, with the initial date
            end_date: datetime, with the final date
            field_s: str or list of str
            save: boolean, True if want to save the cache version
            useCache: boolean: True if want to load a cached version (if available)
            downloadMissing: boolean, True if want to download unavailable data

        Returns
        -------
            data: pandas.DataFrame
        '''
        # 1. Load the Data
        if useCache == True:
            data = self.load(self.generate_filename(symbol_s, start_date, end_date, field_s))
            if data is not None:
                # 1.1 Data was cached so return it
                return data

        # 1.2 Data was not cached before need to load the data from csv files
        df = self.get_data_from_files(symbol_s, start_date, end_date, field_s, downloadMissing)
        if save == True:
            # 1.2.1 Saves the cache version
            self.save(df, self.generate_filename(symbol_s, start_date, end_date, field_s))
        return df

    def get_data_from_files(self, symbol_s, start_date, end_date, field_s, downloadMissing=True):
        '''
        Returns a pandas DataFrame with the data of the symbol/symbols and field
        fields between the specified dates.
        Use directly the information from the csv files
        Optional: If data is not available download the missing data

        Parameters
        ----------
            symbols_s - symbol (str) or list of symbols
            start_date - datetime with the initial date
            end_date - datetime with the final date
            field_s - field (str) or list of fields
            downloadMissing=True - True if want to download missing information from the internet

        Returns
        -------
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
    start_date = datetime(2008, 6, 6)
    end_date = datetime(2009, 12, 31)
    fields = "Close"
    a = da.get_data(symbols, start_date, end_date, fields, useCache=False)
    print(a)

    #da.empty_dirs(delete=True)

