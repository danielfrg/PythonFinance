import math
import numpy as np
import pandas as pd

def total_return(data, col=None):
    '''
    Calculates the total return of a list

    Parameters
    ----------
        data: numpy.array or pandas.Series or pandas.DataFrame
        col=None: if data is pandas.DataFrame use this column to calculate the Total Return

    Returns
    -------
        if data is numpy.array of 1 dim: int with the total return
        if data is numpy.array of 2 dim: numpy.array with the total return of each column
        if data is pandas.Series: int with the total return
        if data is pandas.DataFrame: pandas.DataFrame with the total return of each column
        if data is pandas.DataFrame and col!=None: int with the total return
    '''
    if type(data) is np.ndarray:
        return data[-1] / data[0] - 1
    
    if type(data) is pd.Series or type(data) is pd.TimeSeries:
        return total_return(data.values)

    if type(data) is pd.DataFrame:
        if col is not None:
            return total_return(data[col])
        else:
            series = data.apply(total_return)
            series.name = 'Total Returns'
            return series


def daily_returns(data, col=None):
    '''
    Calculates the daily returns

    Parameters
    ----------
        data: numpy.array or pandas.Series or pandas.DataFrame
        col=None: if data is pandas.DataFrame use this column to calculate the Daily Returns

    Returns
    -------
        if data is numpy.array of 1 dim: numpy.array with the daily returns
        if data is numpy.array of 2 dim: numpy.array with the daily returns of each column
        if data is pandas.Series: pandas.Series with the daily returns
        if data is pandas.DataFrame: pandas.DataFrame with the daily returns of each column
        if data is pandas.DataFrame and col!=None: pandas.Series with the daily returns
    '''

    if type(data) is np.ndarray:
        dr = np.zeros(shape=data.shape)
        dr[1:] = data[1:] / data[0:-1] - 1
        return dr

    if type(data) is pd.Series or type(data) is pd.TimeSeries:
        return pd.Series(daily_returns(data.values), index=data.index, name=data.name + ' Daily Returns')

    if type(data) is pd.DataFrame:
        if col is not None:
            return daily_returns(data[col])
        else:
            df = data.apply(daily_returns)
            return df

def sharpe_ratio(data, col=None):
    '''
    Calculates the sharpe ratio

    Parameters
    ----------
        data - numpy.array or pandas.DataFrame or pandas.Series
        col=None: if data is pandas.DataFrame use this column to calculate the Sharpe Ratio

    Returns
    -------
        if data is numpy.array of 1 dim: int with the sharpe ratio
        if data is numpy.array of 2 dim: numpy.array with the sharpe ratio of each column
        if data is pandas.Series: int with the sharpe ratio
        if data is pandas.DataFrame: pandas.DataFrame with the sharpe ratio of each column
        if data is pandas.DataFrame and col!=None: int with the sharpe ratio
    '''
    if type(data) is np.ndarray:
        dr = daily_returns(data)
        mean = dr.mean(0)
        std = dr.std(0)
        return math.sqrt(len(data)) * mean / std

    if type(data) is pd.Series or type(data) is pd.TimeSeries:
        return sharpe_ratio(data.values)

    if type(data) is pd.DataFrame:
        if col is not None:
            return sharpe_ratio(data[col])
        else:
            series = data.apply(sharpe_ratio)
            series.name = 'Sharpe Ratios'
            return series
