import numpy as np
from sympy import *

t = symbols('t', real=True)
x = exp(t) + cos(t)
y = sin(t)

dx_dt = diff(x, t)
dy_dt = diff(y, t)

dy_dx = dy_dt / dx_dt

result = dy_dx.subs(t, 0)
print(f'dy/dx at t=0: {result}')

if result == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')