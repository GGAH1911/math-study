import sympy as sp
from sympy import log, Rational, floor

# Inequality: log_10(3x) < 2 with domain 3x > 0
# => 3x < 10**2 = 100 => x < 100/3
bound = Rational(100, 3)
max_int = int(floor(bound))
if bound == int(bound):
    max_int -= 1  # strict inequality

def sat(n):
    if 3*n <= 0:
        return False
    return bool(sp.N(log(3*n, 10)) < 2)

if max_int == 33 and sat(max_int) and not sat(max_int + 1):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
