import math
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from finance.utils import Calculator

norm = stats.norm(loc=0.05, scale=0.1)
print(1, 1 - norm.cdf(0.1))

print(2, norm.cdf(-0.1))

print(3, norm.cdf(0.15) - norm.cdf(-0.05))

print(4, norm.ppf(0.01))

print(5, norm.ppf(0.05))

print(6, norm.ppf(0.95))

print(7, norm.ppf(0.99))

# Question 8
X_msft = stats.norm(loc=0.05, scale=0.1)
Y_sbux = stats.norm(loc=0.025, scale=0.05)
x = np.linspace(-0.25, 0.35, 100)

plt.plot(x, X_msft.pdf(x), label='X_msft')
plt.plot(x, Y_sbux.pdf(x), label='Y_sbux')
plt.title('Question 8')
plt.legend()
plt.show()

# Question 9
W0 = 100000
R = stats.norm(loc=0.04, scale=0.09)
print(9, W0 * R.ppf(0.01), W0 * R.ppf(0.05))

# Question 10
W0 = 100000
r = stats.norm(loc=0.04, scale=0.09)
r_1, r_5 = r.ppf(0.01), r.ppf(0.05)
R_1, R_5 = math.exp(r_1) - 1, math.exp(r_5) - 1
print(10, W0 * R_1, W0 * R_5)

# Question 11
q11_amzn = Calculator.ret([38.23, 41.29])
# q11_amzn = Calculator.R(PV=38.23, FV=41.29) # Other option
q11_cost = Calculator.ret([41.11, 41.74])
print(11, q11_amzn, q11_cost)

# Question 12
q12_amzn = Calculator.ret([38.23, 41.29], cc=True)
q12_cost = Calculator.ret([41.11, 41.74], cc=True)
print(12, q12_amzn, q12_cost)

# Question 13
q13_amzn = Calculator.ret([38.23, 41.29], dividends=[0, 0.1])
print(13, q13_amzn, 0.1/41.29)
print(13, (41.29 + 0.1)/38.23 - 1, 0.1/41.29)

# Question 14
q14_ann_ret = Calculator.ann_ret(R=q12_amzn, m=12)
q14_cc_ann_ret = Calculator.ann_ret(R=q12_amzn, cc=True)
print(14, q14_ann_ret, q14_cc_ann_ret)

# Question 15
q15_amzn = 8000/10000
q15_cost = 2000/10000
print(15, q15_amzn, q15_cost)

# Question 16
q16 = q11_amzn * q15_amzn + q11_cost * q15_cost
print(16, q16)





