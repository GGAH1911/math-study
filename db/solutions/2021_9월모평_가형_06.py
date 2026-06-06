import sympy as sp
from sympy import exp, integrate, E

x = sp.Symbol('x')
integrand = (x - 1) * exp(-x)
result = integrate(integrand, (x, 1, 2))
answer = 1/E - 2/(E**2)
if sp.simplify(result - answer) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')