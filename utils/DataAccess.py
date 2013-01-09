import os
import hashlib
import pandas as pd
from datetime import datetime
from finance.utils.FileManager import FileManager

class DataAccess(object):

    path = ''
    '''
    Class to manage the Access to the Data
    
    Features
    --------
        1. Easy access to the data
        2. Serialization of data

    How to use 
    ----------
        Use one: Note: Option 2 overwrites option 1
        1. Set the enviroment variable: FINANCEPATH
        2. Set the Static Variable DataAccess.path

    '''
    def __init__(self):
        if self.path != '':
            self.set_dir(self.path)
        else:
            env_var = os.getenv("FINANCEPATH")
            if env_var is not None:
                self.set_dir(env_var)
            else:
                raise Exception('No path defined')


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
        Empty the directory of csv files. Do not delete the cache files/folder

        Parameters
        ----------
            delete:boolean, True if want to delete the folder too
        '''
        self.file_manager.empty_dir(delete)

    def empty_cache(self, delete=True):
        '''
        Empty the directory of cached files. Does not delete the csv files/folder

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
        Delete both cached and csv files.

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
            data: object (usually pandas.DataFrame), if file was available; None otherwise.
        '''
        h = hashlib.md5()
        h.update(name.encode('utf8'))
        filename = h.hexdigest() + extension

        f = os.path.join(self.cache_dir, filename)
        if os.access(f, os.F_OK):
            return pd.load(f)


    def get_data(self, symbols, start, end, fields='Adj Close', save=True, useCache=True,
                    downloadMissing=True, ignoreMissing=True):
        '''
        Returns a pandas DataFrame with the data of the symbols and field
        fields between the specified dates with the fields specified

        Optional: 
            1. Load a serialized version of the data
            2. Saves a serialized version of the data
            3. If data is not available download the missing data

        Parameters
        ----------
            symbols_s: str or list of str
            start: datetime, with the initial date
            end: datetime, with the final date
            fields: str or list of str
            save: boolean, True if want to save the cache version
            useCache: boolean: True if want to load a cached version (if available)
            downloadMissing: boolean, True if want to download unavailable data
            ignoreMissing=True

        Returns
        -------
            data: pandas.DataFrame
        '''
        # 0. If ask for only one symbols or field convert it to a list of one item
        if type(symbols) == str:
            symbols = [symbols]
        if type(fields) == str:
            fields = [fields]

        # 1. Load the Data, if requested
        filename_id = "%s_%s_%s_%s" % ('_'.join(symbols), start.strftime('%m-%d-%Y'),
                                        end.strftime('%m-%d-%Y'), '-'.join(fields))
        if useCache == True:
            data = self.load(filename_id)
            if data is not None:
                # 1.1 Data was cached before and loaded => return
                return data

        # 1. Data was not cached before need to load the data from csv files
        
        # 1.1 Get the list of filenames from the FileManager
        files = self.file_manager.get_filenames(symbols, start, end, downloadMissing, ignoreMissing)

        # 1.2 We are going to create a pd.DataFrame from a dictionary of pd.Series
        data_dic = {}

        for f, symbol in zip(files, symbols):
            # Create DataFrame from the csv
            new_data = pd.read_csv(os.path.join(self.dir, f))
            # Change the index of the DataFrame to be the date
            new_data = new_data.set_index(pd.to_datetime(new_data['Date']))

            for field in fields:
                # For each field in fields, creates a new column
                colname = ''
                if len(symbols) == 1 and len(fields) == 1:
                    # Single symbol and Single field
                    colname = field
                elif len(symbols) > 1 and len(fields) == 1:
                    # Multiple symbols and single fields
                    colname = symbol
                elif len(symbols) == 1 and len(fields) > 1:
                    # Single symbol and Multiple fields
                    colname = field
                else:
                    # Multiple symbols and multiple fields
                    colname = "%s %s" % (symbol, field)
                # Adds the pd.Series to the dictionary
                data_dic[colname] = new_data[field]

        # 1.4. Create, slice and sort the data
        data = pd.DataFrame(data_dic)
        data = data.sort()[start:end] # Sort because Yahoo Finance data comes reverse

        # Save a cache version if requested
        if save == True:
            self.save(data, filename_id)
        return data
        