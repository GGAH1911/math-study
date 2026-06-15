from sympy import Rational, sqrt

# Problem data
mu = Rational(14)
sigma = Rational(32, 10)      # 3.2
n = 256
a = Rational(137, 10)         # 13.7
b = Rational(142, 10)         # 14.2

# Sample mean standard deviation
sd = sigma / sqrt(n)          # 3.2/16 = 0.2

# Standardize bounds
z_low = (a - mu) / sd
z_high = (b - mu) / sd
assert z_low == Rational(-3, 2), z_low   # -1.5
assert z_high == Rational(1), z_high     # 1.0

# Given table values P(0<=Z<=z)
table = {Rational(1): Rational(3413, 10000),
         Rational(3, 2): Rational(4332, 10000)}

# P(-1.5<=Z<=1.0) = P(0<=Z<=1.5) + P(0<=Z<=1.0)
prob = table[Rational(3, 2)] + table[Rational(1)]

CANDIDATE = 0.7745
if abs(float(prob) - CANDIDATE) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
