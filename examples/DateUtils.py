from datetime import datetime
from finance.utils import DateUtils

all_dates = DateUtils.nyse_dates(list=True)
print(all_dates)

print(DateUtils.nyse_dates(start=datetime(2008,1,1)))

index = DateUtils.search_closer_date(datetime(2009,1,1), all_dates)
print(index, all_dates[index])