from math import erf, sqrt
m = 58
sigma = 10
# P(X <= 50) under N(m, sigma^2)
z = (50 - m) / sigma  # -0.8
P = 0.5 * (1 + erf(z / sqrt(2)))
# Table value 0.2881 corresponds to P(0<=Z<=0.8); so target P(X<=50)=0.5-0.2881=0.2119
target = 0.2119
print('VERIFY_PASS' if abs(P - target) < 5e-4 else 'VERIFY_FAIL')