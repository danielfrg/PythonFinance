import math
import numpy as np
from scipy import stats

A = np.array([[1,4,7], [2,4,8], [6,1,3]])
B = np.array([[4,4,0], [5,9,1], [2,2,5]])
x = np.array([1,2,3])
y = np.array([5,2,7])

# Question 1
print(1, A.T)

# Question 2
print(2, B.T)

# Question 3
print(3, x.T)

# Question 4
print(4, y.T)

# Question 5
print(5, A+B)

# Question 6
print(6, A-B)

# Question 7
print(7, 2*A)

# Question 8
print(8, np.dot(A,x))

# Question 9
print(9, np.dot(y,np.dot(A,x)))

# Question 10
A2 = np.array([[1,1], [2,4]])
x2 = np.array([1,2])
print(10, np.linalg.solve(A2, x2))

# Question 11
x = [1/3,1/3,1/3]
u = np.array([0.01,0.04,0.02])
print(11, (x*u).sum())

# Question 12
V = np.array([[0.1, 0.3, 0.1], [0.3,0.15,-0.2],[0.1,-0.2,0.08]])
print(12, np.dot(x,np.dot(V,x)))


