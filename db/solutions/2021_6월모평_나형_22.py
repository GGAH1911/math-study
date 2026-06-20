import numpy as np
from sympy import sin, symbols, simplify

CANDIDATE = 6

# 원래 함수
x = symbols('x', real=True)
f = 5*sin(x) + 1

# sin(x)의 최댓값은 1
max_sinx = 1
f_at_max = f.subs(sin(x), max_sinx)

if f_at_max == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')