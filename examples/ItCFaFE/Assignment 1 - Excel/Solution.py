import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from finance.utils import DataAccess
from finance.utils import Calculator

da = DataAccess()

# Question 1
symbols = ['SBUX']
start_date = datetime(1993, 3, 31)
end_date = datetime(2008, 3, 31)
fields = 'adjusted_close'
data = da.get_data(symbols, start_date, end_date, fields)
monthly = data.asfreq('M', method='ffill')

monthly.plot()
plt.title('Montly Data')
plt.draw()

# Question 2 and 3
total_return = Calculator.ret(data)
q2 = Calculator.FV(PV=10000, R=total_return)
print(2, q2)

# Question 3
q3 = Calculator.ann_ret(R=total_return, m=1/15)
print(3, q3)

# Question 4
monthly_ln = monthly.apply(np.log)
monthly_ln.plot()
plt.title('Montly Natural Logarithm')
plt.draw()

# Question 5
monthly_returns = Calculator.returns(monthly)
monthly_returns.plot()
plt.title('Montly Returns')
plt.draw()

# Question 7
cc_monthly_returns = Calculator.returns(monthly, cc=True)
cc_monthly_returns.plot()
plt.title('Continuously compounded Montly Returns')
plt.draw()

# Question 6
annual_returns = Calculator.returns(monthly, basedOn=12)
annual_returns.plot()
plt.title('Annual Returns')
plt.draw()

# Question 8
cc_annual_returns = Calculator.returns(monthly, basedOn=12, cc=True)
cc_annual_returns.plot()
plt.title('Continuously compounded Annual Returns')
plt.draw()

# At the end for continous computation
plt.show()
