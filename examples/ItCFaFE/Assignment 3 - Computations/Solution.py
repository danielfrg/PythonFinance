import math
import numpy as np
from scipy import stats

def E(x, prob):
	return np.dot(x, prob)

def VAR(x, prob):
	return E( (x - E(x, prob)) * (x - E(x, prob)) , prob)

x = np.array([1,2,3])
y = np.array([1,2,3])
mat = np.array([[0.1, 0.2, 0], [0.1, 0, 0.2], [0, 0.1, 0.3]])

# Question 1
x_vals = [x, mat.sum(axis=1)]
X = stats.rv_discrete(values=x_vals)
q1 = X.expect()
print(1, q1)

# Question 2
y_vals = [y, mat.sum(axis=0)]
Y = stats.rv_discrete(values=y_vals)
q2 = Y.expect()
print(2, q2)

# Question 3
q3 = X.var()
print(3, q3)

# Question 4
q4 = Y.var()
print(4, q4)

# Question 5
q5 = X.std()
print(5, q5)

# Question 6
q6 = Y.std()
print(6, q6)

# Question 7
X_Ex = np.zeros(9)
Y_Ey = np.zeros(9)
p_XY = np.zeros(9)
it = 0
for i in range(mat.shape[0]):
	for j in range(mat.shape[1]):
		X_Ex[it] = x[i] - q1
		Y_Ey[it] = y[j] - q2
		p_XY[it] = mat[i,j]
		it = it + 1
q7 = (X_Ex * Y_Ey * p_XY).sum()
print(7, q7)

# Question 8
q8 = q7 / (q5 * q6)
print(8, q8)

# Question 9
q9 = y_vals[1][0] == mat[0,0] # One test is enough: P(X=0) != P(X=0|Y=0)
print(9, q9)

# Question 10
W0 = 100000
r = stats.norm(loc=12*0.04, scale=math.sqrt(12) * 0.09)
r_1, r_5 = r.ppf(0.01), r.ppf(0.05)
R_1, R_5 = math.exp(r_1) - 1, math.exp(r_5) - 1
print(10, W0 * R_1, W0 * R_5)


