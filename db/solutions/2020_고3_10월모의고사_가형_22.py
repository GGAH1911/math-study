import numpy as np
from sympy import *

CANDIDATE = 3

# 원래 함수
x = symbols('x')
f = sin(3*x - 6)

# 미분
f_prime = diff(f, x)

# x=2에서의 미분값
result = f_prime.subs(x, 2)
result_simplified = simplify(result)

# 수치 확인
result_numeric = float(result_simplified)

if abs(result_numeric - CANDIDATE) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')