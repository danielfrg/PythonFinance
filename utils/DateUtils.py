import os, inspect
import math
import numpy as np
import pandas as pd
from datetime import datetime


def get_nyse_dates(list=False):
    d = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    filename = os.path.join(d, 'NYSE_dates.txt')

    dates = [datetime.strptime(x ,"b'%m/%d/%Y'") for x in np.loadtxt(filename,dtype=str)]
    if list:
        return dates
    else:
        return pd.TimeSeries(index=dates, data=dates)

def get_nyse_dates_event(date, back_days, forward_days, list=False):
    dates = get_nyse_dates(list=True)

    idx_date = dates.index(date)
    idx_start_date = idx_date - back_days
    idx_end_date = idx_date + forward_days + 1

    dates = dates[idx_start_date:idx_end_date]
    if list:
        return dates
    else:
        return pd.TimeSeries(index=dates, data=dates)
