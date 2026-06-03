from sympy import Rational, sqrt, Abs

sigma = 5
n = 36
z = Rational(258, 100)  # 2.58
E = z * sigma / sqrt(n)  # margin of error

lower = Rational(12, 10)  # 1.2
xbar = lower + E          # sample mean
a = xbar + E              # upper bound

print(f'E = {float(E)}, xbar = {float(xbar)}, a = {float(a)}')

if abs(float(a) - 5.5) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
