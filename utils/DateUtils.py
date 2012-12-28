import math
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from finance.utils import ListUtils

def nyse_dates(start=datetime(2000,1,1), end=datetime.today(),
                insideSearch=True, list=False,
                lookbackDays=0, lookforwardDays=0):
    '''
    Returns the NYSE open dates

    Parameters
    ----------
        start: datetime
        end: datetime
        insideSearch: boolean, TODO
        lookbackDays: int
        lookforwardDays: int
        list: boolean, if want to be returned a python.list
    '''
    start = datetime(start.year, start.month, start.day)
    end = datetime(end.year, end.month, end.day)
    
    if start >= datetime(2000, 1, 1):
        # Get dates from 2000-1-1
        dates = ListUtils.NYSE()
    else:
        # If specify an start date before 2000, ask for all dates
        dates = ListUtils.NYSE(complete=True)

    # Get the indexes to slice the array
    idx_start = 0
    idx_end = len(dates)
    # Get the indexes of the start and end dates
    if start is not datetime(2000,1,1):
        idx_start = search_closer_date(start, dates, searchBack=False)
    if end is not datetime.today():
        idx_end = search_closer_date(end, dates, searchBack=True)
    # Modify the indexes with the lookback and lookforward days
    if lookbackDays is not 0:
        idx_start = idx_start - lookbackDays
    if lookforwardDays is not 0:
        idx_end = idx_end + lookforwardDays
    # Slice the dates using the indexes
    dates = dates[idx_start:idx_end+1]

    if list:
        return dates
    else:
        return pd.TimeSeries(index=dates, data=dates)

def substract(date, ammount):
    dates = nyse_dates()
    idx = search_closer_date(date, dates)
    return dates[idx-ammount]

def add(date, ammount):
    dates = nyse_dates(list=True)
    idx = search_closer_date(date, dates)
    return dates[idx+ammount]

def search_closer_date(date, dates, exact=False, searchBack=True, maxDistance=10):
    '''
    Get the index the closer date given as parameter

    Parameters
    ----------
        date: datetime
        dates: list or np.array or pd.DatetimeIndex, list to look the date on
        searchBack: boolean, True to search for the date into the past
        maxDistance: int, maximum distance (on days) to look for the date
    '''
    # 0. Diferent type of parameters
    if type(dates) == pd.tseries.index.DatetimeIndex:
        dates = dates.to_pydatetime()
    if type(dates) == np.ndarray:
        dates = dates.tolist()

    if exact == False:
        searchBack = -1 if searchBack else 1
        idx = 0
        for i in range(maxDistance):
            try:
                d = date + searchBack * timedelta(days=i)
                return dates.index(d)
            except ValueError:
                pass
    else:
        return dates.index(date)

def nyse_dates_event(date, lookbackDays, lookforwardDays, list=False):
    return nyse_dates(start=date, end=date, lookbackDays=lookbackDays,
                        lookforwardDays=lookforwardDays)
