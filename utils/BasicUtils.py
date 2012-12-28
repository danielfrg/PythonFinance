import math
import numpy as np
import pandas as pd
from copy import deepcopy

def total_return(data):
    '''
    Calculates the total return

    Parameters
    ----------
        data: numpy.array or pandas.Series

    Returns
    -------
        total_return: int, with the total return
    '''
    if type(data) is np.ndarray:
        return (data[-1] / data[0] - 1)[0]
    elif type(data) is pd.Series or type(data) is pd.TimeSeries:
        values = data.values
    elif type(data) is pd.DataFrame:
        return total_return(data[data.columns[0]])

    return values[-1] / values[0] - 1

def daily_returns(data):
    '''
    Calculates the daily returns

    Parameters
    ----------
        data: numpy.array or pandas.Series or pandas.DataFrame

    Returns
    -------
        daily_return: same type as data
    '''
    if type(data) is not np.ndarray:
        values = data.values
    else:
        values = data

    dr = deepcopy(values)
    dr[0] = 0
    dr[1:] = (values[1:] / values[0:-1]) - 1

    if type(data) is np.ndarray:
        return dr
    elif type(data) is pd.core.series.Series:
        ans = pd.Series(dr, index=data.index)
        ans.name = 'Daily Return'
        return ans
    elif type(data) is pd.core.frame.DataFrame:
        ans = pd.DataFrame(dr, index=data.index, columns=data.columns)
        ans.columns.name = 'Daily Return'
        return ans

def sharpe_ratio(data, extraAnswers=False):
    '''
    Calculates the sharpe ratio

    Parameters
    ----------
        data - pandas.DataFrame or pandas.Series
        extraAnswers=False - optional parameter if want more information than just the sharpe_ratio
                                also retuns the mean and standard deviation

    Returns
    -------
        if extraAnswers=False -> int: sharpe ratio
        if extraAnswers=True  -> dictionary: {'sharpe_ratio', 'mean', 'std'}
    '''
    dr = daily_returns(data)
    mean = dr.mean(0)[0]
    std = dr.std(0)[0]
    sr = math.sqrt(len(data)) * mean / std
    if extraAnswers:
        return {'sharpe_ratio': sr, 'mean': mean, 'std': std}
    else:
        return sr
