import numpy as np
from scipy.optimize import fminbound

# Test point 1: a = e^(-3/2), b = 0.5*e^(-3/2)
a1 = np.exp(-1.5)
b1 = 0.5 * np.exp(-1.5)
ab1 = a1 * b1
M = 0.5 * np.exp(-3)

# Test point 2: a = e^(1/2), b = -1.5*e^(1/2)
a2 = np.exp(0.5)
b2 = -1.5 * np.exp(0.5)
ab2 = a2 * b2
m = -1.5 * np.e

# Verify inequalities for a1, b1
x_test = np.linspace(-5, 5, 1000)
lhs1 = -np.exp(-x_test + 1)
rhs1 = np.exp(x_test - 2)
line1 = a1 * x_test + b1

valid1 = np.all(lhs1 <= line1 + 1e-10) and np.all(line1 <= rhs1 + 1e-10)

# Verify inequalities for a2, b2
line2 = a2 * x_test + b2
valid2 = np.all(lhs1 <= line2 + 1e-10) and np.all(line2 <= rhs1 + 1e-10)

# Calculate final answer
M_times_m3 = M * (m ** 3)
abs_product = abs(M_times_m3)
p, q = 16, 27

if valid1 and valid2 and abs(abs_product - q/p) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')