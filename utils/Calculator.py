import math
import numpy as np
import pandas as pd

def FV(PV=1, R=0.01, n=1, m=1):
    '''
    Future Value calculation

    Parameters
    ----------
        PV: int, Present Value
        R: float or list, Rate(s)/Return(s) during each n period
        n: int, Number of compounding periods. No necesary if R is list
        m: int, compounding frequency. For continiously compounding use m=float('inf')
                Example: If n is years then for compund quarterly: m=4

    Returns
    -------
        Future Value: int
    '''
    if type(R) in [int, float, np.float64]:
        if m == float('inf'):
            return PV * math.exp(R * n)
        else:
            return PV * math.pow(1 + R / m, n * m)
    elif type(R) == list:
        ans = PV
        for r in R:
            ans = ans * math.pow(1 + r / m, m)
        return ans

def PV(FV=1, R=0.01, n=1, m=1):
    '''
    Present Value calculation

    Parameters
    ----------
        FV: int, Future Value
        R: float or list, Rate(s)/Return(s) during each n period
        n: int, Number of compounding periods. No necesary if R is list
        m: int, compounding frequency. For continiously compounding use m=float('inf')
                Example: If n is years then for compund quarterly: m=4

    Returns
    -------
        Present Value: int
    '''
    if type(R) in [int, float, np.float64]:
        if m == float('inf'):
            return FV / math.exp(R * n)
        else:
            return FV / math.pow(1 + R / m, n * m)
    elif type(R) == list:
        ans = FV
        for r in R:
            ans = ans / math.pow(1 + r / m, m)
        return ans

def R(PV=1, FV=1, n=1, m=1):
    '''
    Rate/Return

    Parameters
    ----------
        FV: int, Future Value
        PV: int, Present Value
        n: int, Number of periods
        m: int, compounding frequency. TODO: continiously compounding
                Example: If n is years then for compund quarterly: m=4

    Returns
    -------
        Rate: float
    '''
    return m * ( math.pow(FV / PV , 1 / (m * n)) - 1 )

def n(PV=1, FV=1, R=0.1, m=1):
    '''
    Number of periods aka Investment horizon

    Parameters
    ----------
        FV: int, Future Value
        PV: int, Present Value
        R: float, Rate
        m: int, compounding frequency. TODO: continiously compounding
                Example: If n is years then for compund quarterly: m=4

    Returns
    -------
        Investment horizon: int
    '''
    return math.log(FV / PV) / (m * math.log(1 + R / m))

def ear(R=0.1, m=2):
    '''
    Efective Annual Rate

    Parameters
    ----------
        R: float, Rate; for 10%% use 0.1
        m: int, compounding frequency.
                Example: if R is annual, m=2 is semmiannual compounding

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
    Annual Rate
    Example: Convert a semmiannual rate to an annual rate

    Parameters
    ----------
        R: float, Rate; for 10%% use 0.1
        n: int, Number of periods
        m: int, compounding frequency

    Returns
    -------
        Annual Rate: float
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
        if data is pandas.DataFrame and col is None and column == 1: int with the total return
        if data is pandas.DataFrame and col is None and columns > 1: pandas.DataFrame with the total return of each column
        if data is pandas.DataFrame and col is not None: int with the total return
    '''
    if type(data) is np.ndarray:
        if cc:
            return math.log(data[pos] / data[0])
        else:
            return data[pos] / data[0] - 1
    
    if type(data) is pd.Series or type(data) is pd.TimeSeries:
        return total_return(data.values, pos=pos, cc=cc)

    if type(data) is pd.DataFrame:
        if col is None:
            if len(data.columns) == 1:
                return total_return(data[data.columns[0]], pos=pos, cc=cc)
            else:
                series = data.apply(total_return, pos=pos, cc=cc)
                series.name = 'Total Returns'
                return series
        else:
            return total_return(data[col], pos=pos, cc=cc)


def returns(data, basedOn=1, cc=False, col=None):
    '''
    Computes stepwise returns; usually daily

    Parameters
    ----------
        data: numpy.array or pandas.Series or pandas.DataFrame
        cc: boolean, if want the continuously compounded return
        basedOn: Calculate the returns basedOn the previously n entries
            For example if the data is monthly and basedOn=12 is an Annual Return
        col=None: if data is pandas.DataFrame use this column to calculate the Daily Returns

    Returns
    -------
        if data is numpy.array of 1 dim: numpy.array with the daily returns
        if data is numpy.array of 2 dim: numpy.array with the daily returns of each column
        if data is pandas.Series: pandas.Series with the daily returns
        if data is pandas.DataFrame and col is None: pandas.DataFrame with the daily returns of each column
        if data is pandas.DataFrame and col is not None: pandas.Series with the daily returns
    '''

    if type(data) is np.ndarray:
        dr = np.zeros(shape=data.shape)
        if cc:
            dr[basedOn:] = data[basedOn:] / data[0:-basedOn]
            return np.log(dr)
        else:
            dr[basedOn:] = data[basedOn:] / data[0:-basedOn] - 1
            return dr

    if type(data) is pd.Series or type(data) is pd.TimeSeries:
        return pd.Series(returns(data.values, cc=cc,  basedOn=basedOn), index=data.index, name=data.name + ' Daily Returns')

    if type(data) is pd.DataFrame:
        if col is not None:
            return returns(data[col], cc=cc,  basedOn=basedOn)
        else:
            return data.apply(returns, cc=cc, basedOn=basedOn)

def sharpe_ratio(data, col=None, cc=False):
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
        dr = returns(data)
        mean = dr.mean(0)
        std = dr.std(0)
        return math.sqrt(len(data)) * mean / std

    if type(data) is pd.Series or type(data) is pd.TimeSeries:
        return sharpe_ratio(data.values, cc=cc)

    if type(data) is pd.DataFrame:
        if col is not None:
            return sharpe_ratio(data[col], cc=cc)
        else:
            series = data.apply(sharpe_ratio, cc=cc)
            series.name = 'Sharpe Ratios'
            return series
