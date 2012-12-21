import os, inspect
import math
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from finance.utils import NYSE_dates

def nyse_dates(start=None, end=None, insideSearch=True, list=False, useCache=True,
                    lookbackDays=0, lookforwardDays=0):
    '''
    Returns the NYSE open dates

    Parameters
    ----------
        start: datetime
        end: datetime
        insideSearch: boolean, TODO
        list: boolean, if want to be returned a python.list
        useCache: boolean
    '''
    if start is not None or end is not None:
        # Ask for specific dates
        dates = nyse_dates(list=True) # Get all dates
        idx_start = 0
        idx_end = len(dates)
        # Get the indexes of the start and end dates
        if start is not None:
            idx_start = get_idx_date(start, searchBack=False)
        if end is not None:
            idx_end = get_idx_date(end)
        # Modify the indexes with the lookback and lookforward days
        if lookbackDays is not 0:
            idx_start = idx_start - lookbackDays
        if lookforwardDays is not 0:
            idx_end = idx_end + lookforwardDays
        dates = dates[idx_start:idx_end+1]
    else:
        # Ask for all dates
        if useCache:
            dates = NYSE_dates.all_dates
        else :
            self_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
            filename = os.path.join(self_dir, 'NYSE_dates.txt')
            dates = [datetime.strptime(x ,"b'%m/%d/%Y'") for x in np.loadtxt(filename,dtype=str)]

    if list:
        return dates
    else:
        return pd.TimeSeries(index=dates, data=dates)


def get_idx_date(date, searchBack=True, maxDistance=10, customDates=None):
    '''
    Get the index the closer date given as parameter

    Parameters
    ----------
        date: datetime
        searchBack: boolean, True to search for the date into the past
        maxDistance: int, maximum distance (on days) to look for the date
        customDates: array, if want to look for an index on a custom array of dates
                            instead of the NYSE dates
    '''
    if customDates is not None:
        dates = customDates
    else:
        dates = nyse_dates(list=True)

    searchBack = -1 if searchBack else 1
    idx = 0
    for i in range(maxDistance):
        try:
            d = date + searchBack * timedelta(days=i)
            idx = dates.index(d)
            break # If didn't generate error then date was founded
        except ValueError:
            pass

    return idx

def nyse_dates_event(date, lookbackDays, lookforwardDays, list=False):
    return nyse_dates(start=date, end=date, lookbackDays=lookbackDays,
                        lookforwardDays=lookforwardDays)

