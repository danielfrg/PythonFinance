import math
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from finance.utils import ListUtils

def nyse_dates(start=datetime(2007,1,1), end=datetime.today(),
                insideSearch=True, lookbackDays=0, lookforwardDays=0,
                series=False):
    '''
    Returns the NYSE open dates

    Parameters
    ----------
        start: datetime, start date of the range (incluse)
            Default value:
                datetime(2007,1,1) 
                datetime(1962,7,5) if end is lower than 2007-1-1
        end: datetime, end date of the range (incluse)
            Default value: datetime.today()
        insideSearch: boolean, TODO
        lookbackDays: int
        lookforwardDays: int
        series: boolean, if want to be returned a pandas.series

    Returns
    -------
        dates: list of dates or pandas.Series
    '''
    start = datetime(start.year, start.month, start.day)
    end = datetime(end.year, end.month, end.day)
    
    if start < datetime(2007, 1, 1) or end < datetime(2007, 1, 1):
        # If specify an start date or end date before 2007-1-1
        dates = ListUtils.NYSE(complete=True)

        if end < datetime(2007, 1, 1) and start == datetime(2007, 1, 1):
            # In case only specify an end date lower than 2007-1-1
            start = dates[0]
    else:
        # Get dates from 2007-1-1
        dates = ListUtils.NYSE()

    # Get the indexes to slice the array
    idx_start = 0
    idx_end = len(dates)
    # Get the indexes of the start and end dates
    if start is not datetime(2007,1,1):
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

    if series:
        return pd.TimeSeries(index=dates, data=dates)
    else:
        return dates

def nyse_add(date, amount):
    '''
    Add a number of date to a current date using the NYSE open dates

    Parameters
    ----------
        date: datetime
        amount: int, how many days wants to add
    '''
    dates = nyse_dates(start=date)
    idx = search_closer_date(date, dates)
    return dates[idx+amount]

def nyse_substract(date, amount):
    '''
    Substracts a number of date to a current date using the NYSE open dates

    Parameters
    ----------
        date: datetime
        amount: int, how many days wants to substract

    Returns
    -------
        date: datetime
    '''
    dates = nyse_dates(end=date)
    idx = search_closer_date(date, dates)
    return dates[idx-amount]


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

def nyse_dates_event(eventDate, lookbackDays, lookforwardDays, estimationPeriod, pastEvent=True):
    '''
    Special Case of DateUtils.nyse_dates() returns the dates around an event

    Parameters
    ----------
        eventDate: datetime
        lookbackDays: int
        lookforwardDays: int
        estimationPeriod: int

    Returns
    -------
        dates: list of dates or pandas.Series
    '''
    if pastEvent:
        return nyse_dates(start=eventDate, end=eventDate, 
                        lookbackDays=estimationPeriod+lookbackDays,
                        lookforwardDays=lookforwardDays)
    else:
        return nyse_dates(start=eventDate, end=eventDate, 
                        lookbackDays=lookbackDays,
                        lookforwardDays=estimationPeriod+lookforwardDays)
