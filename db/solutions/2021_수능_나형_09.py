import numpy as np

def f(x):
    return x**3 - 3*x**2 + 2*x + 2

def f_prime(x):
    return 3*x**2 - 6*x + 2

# 점 A(0, 2)에서의 접선 기울기
m_tangent = f_prime(0)

# 수직선의 기울기
m_perp = -1 / m_tangent

# x절편 구하기: 직선 y = m_perp * x + 2에서 y = 0
x_intercept = -2 / m_perp

# 검증: x절편에서 직선이 y = 0을 지나는가?
y_at_intercept = m_perp * x_intercept + 2

if abs(y_at_intercept) < 1e-10 and abs(x_intercept - 4) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')