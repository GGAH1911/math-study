import sympy as sp
import numpy as np

x = sp.Symbol('x')
equation = 2**x + 2*x**2 - 2

x1 = float(sp.nsolve(equation, -0.85))
x2 = float(sp.nsolve(equation, 0.53))

if x1 > x2:
    x1, x2 = x2, x1

y1 = 2**x1
y2 = 2**x2

eq1_check = abs(2**x1 - (-2*x1**2 + 2)) < 1e-9
eq2_check = abs(2**x2 - (-2*x2**2 + 2)) < 1e-9

cond_a = x2 > 0.5
cond_b = y2 - y1 < x2 - x1
cond_c = np.sqrt(2)/2 < y1*y2 < 1

if eq1_check and eq2_check and cond_a and cond_b and cond_c:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')