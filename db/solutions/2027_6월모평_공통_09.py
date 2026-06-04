from sympy import symbols, integrate, solve, simplify
import numpy as np

t, k = symbols('t k')
v1 = t**2 - t
v2 = t

# 위치 함수 구하기
x_P = integrate(v1, (t, 0, k))
x_Q = integrate(v2, (t, 0, k))

# k=3일 때 확인
k_val = 3
x_P_at_3 = x_P.subs(k, k_val)
x_Q_at_3 = x_Q.subs(k, k_val)

if x_P_at_3 == x_Q_at_3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'x_P(3) = {x_P_at_3}, x_Q(3) = {x_Q_at_3}')