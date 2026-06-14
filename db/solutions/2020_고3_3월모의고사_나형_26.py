import sympy as sp
from sympy import sqrt, limit, oo, symbols

CANDIDATE = 6

t = symbols('t', real=True, positive=True)

# 이차함수 f(x) = (x+2)(x-t+1)
# P(t, t+2)는 곡선 위의 점
# f(t) = (t+2)(t-t+1) = (t+2)(1) = t+2 ✓

# Q는 y축 교점: f(0) = (0+2)(0-t+1) = 2(1-t) = 2-2t
Q_y = 2 - 2*t

# A(-2, 0), P(t, t+2)
AP = sqrt((t - (-2))**2 + ((t+2) - 0)**2)
AP_simplified = sqrt((t+2)**2 + (t+2)**2)
AP_expr = sqrt(2) * (t + 2)  # t > 0일 때

# A(-2, 0), Q(0, 2-2t)
AQ = sqrt((0 - (-2))**2 + (Q_y - 0)**2)
AQ_simplified = sqrt(4 + (2-2*t)**2)
AQ_expanded = sqrt(4 + 4*(1-t)**2)
AQ_expr = 2*sqrt(t**2 - 2*t + 2)

# 극한 계산
expr = sqrt(2) * AP_expr - AQ_expr
expr_simplified = 2*(t+2) - 2*sqrt(t**2 - 2*t + 2)

result = limit(expr_simplified, t, oo)

if result == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Expected: {CANDIDATE}, Got: {result}')