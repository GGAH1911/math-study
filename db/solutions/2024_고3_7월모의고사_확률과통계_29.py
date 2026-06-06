import numpy as np
from scipy.stats import norm

m = 4
sigma = 10

# X ~ N(4, 1)
mu_X = m
std_X = 1

# Y ~ N(40, 100)
mu_Y = m**2 + 2*m + 16
std_Y = sigma

k = 70

# P(X >= 1)
prob_X = 1 - norm.cdf(1, loc=mu_X, scale=std_X)

# P(Y <= k)
prob_Y = norm.cdf(k, loc=mu_Y, scale=std_Y)

print(f'P(X >= 1) = {prob_X:.10f}')
print(f'P(Y <= k) = {prob_Y:.10f}')
print(f'Difference = {abs(prob_X - prob_Y):.2e}')

if abs(prob_X - prob_Y) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')