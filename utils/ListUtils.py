


def NYSE(complete=False):
    if complete == False:
        from finance.utils import NYSE_dates
        return NYSE_dates.all_dates
    else:
        import os, inspect
        import numpy as np
        from datetime import datetime
        self_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        filename = os.path.join(self_dir, './lists/NYSE_dates.txt')
        return [datetime.strptime(x ,"b'%m/%d/%Y'") for x in np.loadtxt(filename,dtype=str)]

def SP500(year=2012):
    if year == 2012:
        from finance.utils import SP500_2012
        return SP500_2012.all_symbols
    elif year == 2008:
        from finance.utils import SP500_2008
        return SP500_2008.all_symbols