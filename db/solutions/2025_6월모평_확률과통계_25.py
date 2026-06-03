from math import comb
import sympy as sp

x = sp.Symbol('x')
poly = (x**2 - 2)**5
expanded = sp.expand(poly)
coeff_x6 = expanded.coeff(x, 6)

if coeff_x6 == 40:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')