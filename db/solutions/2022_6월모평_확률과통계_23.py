from math import comb
from sympy import symbols, expand

x = symbols('x')
expr = (2*x + 1)**5
expanded = expand(expr)
coeff_x3 = expanded.coeff(x, 3)
print('VERIFY_PASS' if coeff_x3 == 80 else 'VERIFY_FAIL')