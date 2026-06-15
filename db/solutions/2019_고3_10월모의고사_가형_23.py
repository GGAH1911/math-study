import math
from sympy import *

CANDIDATE = 2

# 원래 함수
x = symbols('x')
f = sin(x) - sqrt(3)*cos(x)

# 도함수
f_prime = diff(f, x)

# x = π/3에서의 값
x_val = pi/3
result = f_prime.subs(x, x_val)
result_simplified = simplify(result)

# 수치 계산
result_numerical = float(result_simplified)

if abs(result_numerical - CANDIDATE) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')