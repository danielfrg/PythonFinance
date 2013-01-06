import math
import numpy as np
import pandas as pd

def FV(PV=1, R=0.01, n=1, m=1):
    '''
    Future Value

    Parameters
    ----------
        PV: int, Present Value
        R: float, Rate; for 10%% use 0.1
        n: int, Number of periods
        m: int, compounding frequency: m times per period. 
                For continiously compounding use m=float('inf')
                If n is years then: 
                    compund quarterly: m=4
                    compund weekly: m=52 
                    compund daily: m=365

    Returns
    -------
        Future Value: int
    '''
    if m == float('inf'):
        return PV * math.exp(R * n)
    else:
        return PV * math.pow(1 + (R / m), n * m)

def PV(FV=1, R=0.01, n=1, m=1):
    '''
    Present Value

    Parameters
    ----------
        FV: int, Future Value
        R: float, Rate; for 10%% use 0.1
        n: int, Number of periods
        m: int, compounding frequency: m times per period

    Returns
    -------
        Present Value: int
    '''
    if m == float('inf'):
        return FV / math.exp(R * n)
    else:
        return FV / math.pow(1 + (R / m), n * m)

def R(PV=1, FV=1, n=1):
    '''
    Rate

    Parameters
    ----------
        FV: int, Future Value
        PV: int, Present Value
        n: int, Number of periods

    Returns
    -------
        Rate: float
    '''
    return math.pow(FV / PV , 1 / n) - 1

def n(PV=1, FV=1, R=0.1):
    '''
    Investment horizon

    Parameters
    ----------
        FV: int, Future Value
        PV: int, Present Value
        R: float, Rate

    Returns
    -------
        Investment horizon: int
    '''
    return math.log(FV / PV) / math.log(1 + R)

def ear(R=0.1, m=1):
    '''
    Efective Annual Rate

    Parameters
    ----------
        R: float, Rate; for 10%% use 0.1
        n: int, Number of periods
        m: int, compounding frequency: m times per period

    Returns
    -------
        Efective Annual Rate: float
    '''
    if m == float('inf'):
        return math.exp(R) - 1
    else:
        return math.pow(1 + (R / m), m) - 1

def ar(R=0.1, m=1, cc=False):
    '''
    Efective Annual Rate

    Parameters
    ----------
        R: float, Rate; for 10%% use 0.1
        n: int, Number of periods
        m: int, compounding frequency: m times per period

    Returns
    -------
        Efective Annual Rate: float
    '''
    if cc:
        return R * m
    if m == float('inf'):
        return math.exp(R) - 1
    else:
        return math.pow(1 + R, m) - 1

def total_return(data, pos=-1, cc=False, col=None):
    '''
    Calculates the total return of a list

    Parameters
    ----------
        data: numpy.array or pandas.Series or pandas.DataFrame
        pos: int, calculate the return of that position (index): if -1 then calculates the total return
        cc: boolean, if want the continuously compounded return
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
        if cc:
            return math.log(data[pos] / data[0])
        else:
            return data[pos] / data[0] - 1
    
    if type(data) is pd.Series or type(data) is pd.TimeSeries:
        return total_return(data.values, pos=pos, cc=cc)

    if type(data) is pd.DataFrame:
        if col is not None:
            return total_return(data[col], pos=pos, cc=cc)
        else:
            series = data.apply(total_return, pos=pos, cc=cc)
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
