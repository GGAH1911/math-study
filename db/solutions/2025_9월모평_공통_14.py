import math
from sympy import *

n_vals = [1, 2, 3]
total = 0

for n in n_vals:
    two_a = Rational(3*n, 2**n - 1)
    a = log(two_a, 2)
    b = a + n
    two_b = 2**b
    x_n = 2**(a + n)
    x_n_formula = Rational(3*n * 2**n, 2**n - 1)
    assert simplify(x_n - x_n_formula) == 0
    total += x_n_formula

result = total
expected = Rational(170, 7)
assert result == expected, f'{result} != {expected}'
print('VERIFY_PASS')