import math
import pandas as pd
from finance.sim import MarketSimulator

def total_return(df, field=None):
    if field is None:
        return df.values[-1][0] / df.values[0][0] - 1
    else:
        return df[field].values[-1] / df[field].values[0] - 1

def daily_returns(df, field=None):
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
    dr = daily_returns(df, field)
    mean = dr.mean(0)[0]
    std = dr.std(0)[0]
    sr = math.sqrt(len(df)) * mean / std
    if extraAnswers:
        return {'sharpe_ratio': sr, 'mean': mean, 'std': std}
    else:
        return sr
