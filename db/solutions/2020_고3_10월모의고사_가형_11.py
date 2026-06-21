import sympy as sp
import numpy as np
from sympy import sin, cos, pi, sqrt, solve, simplify

x = sp.Symbol('x')
eq = sp.Eq(sin(x), sqrt(3)*(1 + cos(x)))

solutions = []
for x_val in [pi, 2*pi/3, 4*pi/3]:
    lhs = sin(x_val)
    rhs = sqrt(3)*(1 + cos(x_val))
    if simplify(lhs - rhs) == 0:
        solutions.append(x_val)

total = sum(solutions)
expected = 5*pi/3

if simplify(total - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')