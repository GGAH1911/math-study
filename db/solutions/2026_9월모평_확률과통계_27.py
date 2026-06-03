from fractions import Fraction
from itertools import product

die_a = [1, 2, 2, 3]
die_b = [1, 2, 2, 3]
outcomes = list(product(die_a, die_b))
n = len(outcomes)

x_fracs = [Fraction(abs(a - b)) for a, b in outcomes]
E_X = sum(x_fracs) / n
E_X2 = sum(x**2 for x in x_fracs) / n
V_X = E_X2 - E_X**2

if V_X == Fraction(7, 16):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'V(X) = {V_X}')