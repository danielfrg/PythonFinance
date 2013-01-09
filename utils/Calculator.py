import math
import numpy as np
import pandas as pd

''' ------------------------------------------------------------------------------------ '''
'''                                TIME VALUE OF MONEY                                   '''
''' ------------------------------------------------------------------------------------ '''

def FV(PV=1, R=0.01, n=1, m=1, cc=False, ret_list=False):
    '''
    Future Value calculation

    Parameters
    ----------
        PV: int, Present Value
        R: float or list or pandas.Series, return(s) during each n period
        n: int, Number of compounding periods. No necesary if R is list
        m: int, compounding frequency. For continiously compounding use m='inf'
                Example: If n is years then for compund quarterly: m=4
        ret_list: boolean, if R is a list then return a list of each Future Value

    Returns
    -------
        Future Value: int
    '''
    if type(R) in [int, float, np.float64]:
        if m == 'inf' or m == float('inf') or cc:
            return PV * math.exp(R * n)
        else:
            return PV * math.pow(1 + R / m, n * m)
    elif type(R) in (list, np.ndarray):
        ans = [PV]
        for (r, i) in zip(R, range(1, len(R) + 1)):
            ans.append(FV(PV=ans[i-1], R=r, m=m))

        if ret_list:
            return ans[1:]
        else:
            return ans[-1]
    elif type(R) in (pd.Series, pd.TimeSeries):
        ans = FV(PV=PV, R=R.values, ret_list=ret_list)
        if ret_list:
            return pd.Series(ans, index=R.index, name='Future Value')
        return ans

def PV(FV=1, R=0.01, n=1, m=1, cc=False, ret_list=True):
    '''
    Present Value calculation

    Parameters
    ----------
        FV: int, Future Value
        R: float or list, return(s) during each n period
        n: int, Number of compounding periods. No necesary if R is list
        m: int, compounding frequency. For continiously compounding use m='inf'
                Example: If n is years then for compund quarterly: m=4

    Returns
    -------
        Present Value: int
    '''
    if type(R) in [int, float, np.float64]:
        if m == 'inf' or m == float('inf') or cc:
            return FV / math.exp(R * n)
        else:
            return FV / math.pow(1 + R / m, n * m)
    elif type(R) in (list, np.ndarray):
        ans = [FV]
        for (r, i) in zip(R[::-1], range(1, len(R) + 1)):
            ans.append(PV(FV=ans[i-1], R=r, m=m))

        if ret_list:
            return ans[::-1][1:]
        else:
            return ans[-1]
    elif type(R) in (pd.Series, pd.TimeSeries):
        ans = PV(FV=FV, R=R.values, ret_list=ret_list)
        if ret_list:
            return pd.Series(ans, index=R.index, name='Present Value')
        return ans

def R(PV=1, FV=1, n=1, m=1, cc=False):
    '''
    Compound return of each n period; usually annual
    Example: use it to calculate a Compound Annual Growth Return

    Parameters
    ----------
        FV: int, Future Value
        PV: int, Present Value
        n: int, Number of periods
        m: int, compounding frequency. For continiously compounding use m='inf'
                Example: If n is years then for compund quarterly: m=4

    Returns
    -------
        Return: float
    '''
    if m == 'inf' or m == float('inf') or cc:
        return math.log(FV / PV) / n
    else:
        return m * ( math.pow(FV / PV , 1 / (m * n)) - 1 )

def n(PV=1, FV=1, R=0.1, m=1, cc=False):
    '''
    Investment horizon: Number of periods (n)

    Parameters
    ----------
        FV: int, Future Value
        PV: int, Present Value
        R: float, Return
        m: int, compounding frequency. For continiously compounding use m='inf'
                Example: If n is years then for compund quarterly: m=4

    Returns
    -------
        Investment horizon: int
    '''
    if m == 'inf' or m == float('inf') or cc:
        return math.log(FV / PV) / R
    else:
        return math.log(FV / PV) / (m * math.log(1 + R / m))

def eff_ret(R=0.01, m=2, cc=False):
    '''
    Efective Return
    Use for: What is the Annual rate that equates a rate R with a frequency of m

    Parameters
    ----------
        R: float, Return; for 10%% use 0.1
        m: int, compounding frequency. For continiously compounding use m='inf'
                Example: if R is annual, m=2 is semmiannual compounding

    Returns
    -------
        Efective Annual Return: float
    '''
    if m == 'inf' or m == float('inf') or cc:
        return math.exp(R) - 1
    else:
        return math.pow(1 + (R / m), m) - 1

def ann_ret(R=0.1, m=1, cc=False):
    '''
    Annualize Return
    Example: Convert a semmiannual return to an annual return

    Parameters
    ----------
        R: float, Return; for 10%% use 0.1
        n: int, Number of periods. For continiously compounding use m='inf'
        m: int, compounding frequency

    Returns
    -------
        Annual Return: float
    '''
    if cc:
        return R * m
    if m == 'inf':
        return math.exp(R) - 1
    else:
        return math.pow(1 + R, m) - 1

''' ------------------------------------------------------------------------------------ '''
'''                                      ASSET RETURNS                                   '''
''' ------------------------------------------------------------------------------------ '''

def ret(data, pos=-1, cc=False, col=None):
    '''
    Calculates the total return

    Parameters
    ----------
        data: numpy.array or pandas.Series or pandas.DataFrame
        pos: int, calculate the return of that position (index): if 1 then calculates the total return
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
        return ret(data.values, pos=pos, cc=cc)

    if type(data) is pd.DataFrame:
        if col is None:
            if len(data.columns) == 1:
                return ret(data[data.columns[0]], pos=pos, cc=cc)
            else:
                series = data.apply(ret, pos=pos, cc=cc)
                series.name = 'Total Returns'
                return series
        else:
            return ret(data[col], pos=pos, cc=cc)


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
            # return np.log(data[basedOn:] / data[0:-basedOn])
            dr[basedOn:] = np.log(data[basedOn:] / data[0:-basedOn])
            return dr
        else:
            # return data[basedOn:] / data[0:-basedOn] - 1
            dr[basedOn:] = data[basedOn:] / data[0:-basedOn] - 1
            return dr

    if type(data) is pd.Series or type(data) is pd.TimeSeries:
        ans = returns(data.values, cc=cc,  basedOn=basedOn)
        return pd.Series(ans, index=data.index, name=data.name + ' Daily Returns')

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
