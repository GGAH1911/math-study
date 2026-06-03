import math
from math import sqrt, pi, exp, erf

def Phi(z):
    return 0.5*(1+erf(z/sqrt(2)))

# Use a=1 (any positive a works by scaling). Derived: mu_X=2a, sigma=2a, mu_Y=a.
a = 1.0
mu_X = 2*a
sigma = 2*a
mu_Y = a

def f(x):
    return (1/(sigma*sqrt(2*pi)))*exp(-(x-mu_X)**2/(2*sigma**2))

def g(x):
    return (1/(sigma*sqrt(2*pi)))*exp(-(x-mu_Y)**2/(2*sigma**2))

# Check original conditions
cond1 = math.isclose(f(a), f(3*a), rel_tol=1e-9)
cond2 = math.isclose(f(3*a), g(2*a), rel_tol=1e-9)
P_Y_le_2a = Phi((2*a-mu_Y)/sigma)
cond3 = math.isclose(P_Y_le_2a, 0.6915, abs_tol=5e-4)

# Compute target probability using standard normal table values
# P(0 <= X <= 3a) with table values 0.3413 (z=1), 0.1915 (z=0.5)
target_exact = Phi((3*a-mu_X)/sigma) - Phi((0-mu_X)/sigma)
target_table = 0.3413 + 0.1915
answer_value = 0.5328

cond4 = math.isclose(target_table, answer_value, abs_tol=1e-9)
cond5 = math.isclose(target_exact, answer_value, abs_tol=2e-3)

if cond1 and cond2 and cond3 and cond4 and cond5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
