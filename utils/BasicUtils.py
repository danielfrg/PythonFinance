import math
import pandas as pd

def total_return(df, field=None):
    '''
    Calculates the total return
    Parameters:
        df - pandas.DataFrame or pandas.Series
        field=None - optinal parameter with column name of the target
    Returns:
        int
    '''
    if field is None:
        return df.values[-1][0] / df.values[0][0] - 1
    else:
        return df[field].values[-1] / df[field].values[0] - 1

def daily_returns(df, field=None):
    '''
    Calculates the daily returns
    Parameters:
        df - pandas.DataFrame or pandas.Series
        field=None - optinal parameter with column name of the target
    Returns:
        pandas.dataFrame: index equal to the original - columns:['Daily Return']
    '''
    ans = pd.DataFrame(None, index=df.index, columns=['Daily Return'])
    ans['Daily Return'][0] = 0

    i = 0
    for idx, row in df.iterrows():

        if i == 0:
            first_it = False
        else:
            ret = 0
            if field is None:
                ret = df.values[i][0] / df.values[i-1][0] - 1
            else:
                ret = df[field].values[i] / df[field].values[i-1] - 1
            ans['Daily Return'][i] = ret
        i = i + 1

    return ans

def sharpe_ratio(df, field=None, extraAnswers=False):
    '''
    Calculates the sharpe ratio
    Parameters:
        df - pandas.DataFrame or pandas.Series
        field=None - optinal parameter with column name of the target
        extraAnswers=False - optional parameter if want more information than just the sharpe_ratio
                                also retuns the mean and standard deviation
    Returns:
        int (if extraAnswers=False) - with the sharpe ratio
        dictionary (if extraAnswers=True) - with {'sharpe_ratio', 'mean', 'std'}
    '''
    dr = daily_returns(df, field)
    mean = dr.mean(0)[0]
    std = dr.std(0)[0]
    sr = math.sqrt(len(df)) * mean / std
    if extraAnswers:
        return {'sharpe_ratio': sr, 'mean': mean, 'std': std}
    else:
        return sr
