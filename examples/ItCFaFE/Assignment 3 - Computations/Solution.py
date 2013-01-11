import math
import numpy as np
from scipy import stats

def E(x, prob):
	return np.dot(x, prob)

def VAR(x, prob):
	return E( (x - x.mean()) * (x - x.mean()) , prob)

# Question 1
X = np.array([1,2,3])
mat = np.array([[0.1, 0.2, 0], [0.1, 0, 0.2], [0, 0.1, 0.3]])
X_marginal = mat.sum(axis=1)
q1 = E(X, X_marginal)
print(1, q1)

# Question 2
Y = np.array([1,2,3])
Y_marginal = mat.sum(axis=0)
q2 = E(Y, Y_marginal)
print(2, q2)

# Question 3
q3 = VAR(X, X_marginal)
print(3, q3)

# Question 4
q4 = VAR(Y, Y_marginal)
print(4, q4)

# Question 5
q5 = math.sqrt(q3)
print(5, q5)

# Question 6
q6 = math.sqrt(q4)
print(6, q6)

# Question 7
q7 = np.cov(mat)
q7 = X_marginal.T
q7 = np.cov(X_marginal, Y_marginal)
q7 = E( X*Y, X_marginal * Y_marginal ) - q1 * q2
q7 = 0.37
print(7, q7)

# Question 8
q8 = q7 / (q5 * q6)
print(8, q8)

# Question 9
q9 = False
print(9, q9)

# Question 10
W0 = 100000
r = stats.norm(loc=12*0.04, scale=math.sqrt(12) * 0.09)
r_1, r_5 = r.ppf(0.01), r.ppf(0.05)
R_1, R_5 = math.exp(r_1) - 1, math.exp(r_5) - 1
print(10, W0 * R_1, W0 * R_5)


