import math
from sympy import symbols, sqrt, simplify, solve

# 6^{-a} = 6/5일 때 검증
inv_a = 6/5
a_val = symbols('a_val', real=True, positive=True)

# A(a, 6^{-a}), B(a+1, 6^{-(a+1)})
y_A = inv_a
y_B = inv_a * (1/6)

# 거리 계산
dist_squared = 1**2 + (y_B - y_A)**2
print(f'|AB|^2 = {dist_squared}')

# 정사각형 대각선 길이의 제곱은 2
if abs(dist_squared - 2) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')