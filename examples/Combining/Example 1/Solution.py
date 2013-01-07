import pandas as pd
from finance.utils import Calculator

# Create the data

data = [['December, 2004', 31.18],
['January, 2005', 27.00],
['February, 2005', 25.91],
['March, 2005', 25.83],
['April, 2005', 24.76],
['May, 2005', 27.40],
['June, 2005', 25.83],
['July, 2005', 26.27],
['August, 2005', 24.51],
['September, 2005', 25.05],
['October, 2005', 28.28],
['November, 2005', 30.45],
['December, 2005', 30.51]]

starbucks = pd.DataFrame(data, columns=['Date', 'Value']).set_index('Date')['Value']

'''
Question 1: Using the data in the table, what is the simple monthly return between the 
end of December 2004 and the end of January 2005?
Ans: -13.40%
'''
q1 = Calculator.total_return(starbucks, pos=1)
print(1, q1)

'''
Question 2: If you invested $10,000 in Starbucks at the end of December 2004, how much 
would the investment be worth at the end of January 2005?
Ans: $8659.39
'''
q2 = Calculator.FV(PV=10000, R=q1) # n=1 is the default
print(2, q2)

'''
Question 3: Using the data in the table, what is the continuously compounded monthly 
return between December 2004 and January 2005?
Ans: -14.39%
'''
q3 = Calculator.total_return(starbucks, pos=1, cc=True)
print(3, q3)

'''
Question 4: Assuming that the simple monthly return you computed in Question 1 is 
the same for 12 months, what is the annual return with monthly compounding?
Ans: -82.22%
'''
q4 = Calculator.ar(R=q1, m=12)
print(4, q4)

'''
Question 5: Assuming that the continuously compounded monthly return you computed 
in Question 3 is the same for 12 months, what is the continuously compounded annual return?
Ans: -172.72%
'''
q5 = Calculator.ar(R=q3, m=12, cc=True)
print(5, q5)

'''
Question 6: Using the data in the table, compute the actual simple annual return between 
December 2004 and December 2005.
Ans: -2.14%
'''
q6 = Calculator.total_return(starbucks) # pos=-1 is the default
print(6, q6)

'''
Question 7: If you invested $10,000 in Starbucks at the end of December 2004, how much 
would the investment be worth at the end of December 2005?
Ans: $9785.11
'''
q7 = Calculator.FV(PV=10000, R=q6)
print(7, q7)

'''
Question 8: Using the data in the table, compute the actual annual continuously compounded 
return between December 2004 and December 2005.
Ans: -2.17%
'''
q8 = Calculator.total_return(starbucks, cc=True)
print(8, q8)