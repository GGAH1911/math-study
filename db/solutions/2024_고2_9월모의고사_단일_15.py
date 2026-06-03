from sympy import symbols, solve, diff, Rational

x = symbols('x', real=True)
a_val = 3

# 원래 함수
f = 4**(x - a_val) - 8 * 2**(x - a_val)

# t = 2^(x-a) 치환
t = symbols('t', positive=True)
g = t**2 - 8*t

# 최솟값 위치
t_min = solve(diff(g, t), t)[0]  # 4
b_val = g.subs(t, t_min)         # -16

# x=5에서 최소 확인
from sympy import log
x_at_tmin = solve(2**(x - a_val) - t_min, x)[0]  # should be 5

a_plus_b = a_val + b_val

if x_at_tmin == 5 and int(a_plus_b) == -13:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
