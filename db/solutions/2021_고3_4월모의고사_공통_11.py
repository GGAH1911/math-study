import numpy as np
from sympy import cos, sin, pi, symbols, simplify, solve

x = symbols('x', real=True)
eq = 2*cos(x)**2 - sin(pi + x) - 2

solutions = [pi/6, 5*pi/6, pi]
verified = True

for sol in solutions:
    val = eq.subs(x, sol)
    if abs(float(val)) > 1e-10:
        verified = False
        break

if verified:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')