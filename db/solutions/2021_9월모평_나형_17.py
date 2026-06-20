import sympy as sp
import numpy as np

# 기호 정의
x_sym = sp.Symbol('x', real=True, positive=True)

# 함수 정의
AB = 2 * sp.log(x_sym, 2)
AC = sp.log(16/x_sym, 4)

# AC 정리: log_4(16/x) = 2 - log_4(x) = 2 - log_2(x)/2
AC_simplified = 2 - sp.log(x_sym, 2) / 2

# 넓이
S_expr = sp.Rational(1, 2) * AB * AC_simplified
S_simplified = sp.simplify(S_expr)

# t = log_2(x)로 치환
t = sp.Symbol('t', real=True)
S_t = 2*t - t**2/2

# 미분
dS_dt = sp.diff(S_t, t)

# 임계점
critical_points = sp.solve(dS_dt, t)
t_max = 2

# a와 M
a_value = 2**t_max
M_value = S_t.subs(t, t_max)
answer_value = a_value + M_value

# 검증
if a_value == 4 and M_value == 2 and answer_value == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')