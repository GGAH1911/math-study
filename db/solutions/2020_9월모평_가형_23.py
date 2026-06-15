import sympy as sp
from sympy import exp, symbols, diff

CANDIDATE = 4

t, a, b = symbols('t a b', real=True)

# 위치함수 정의
x = sp.Rational(1,2) * exp(2*(t-1)) - a*t
y = b * exp(t-1)

# 속도(미분)
vx = diff(x, t)
vy = diff(y, t)

# t=1에서의 속도
vx_at_1 = vx.subs(t, 1)
vy_at_1 = vy.subs(t, 1)

# 주어진 조건: 속도 = (-1, 2)
eq1 = sp.Eq(vx_at_1, -1)
eq2 = sp.Eq(vy_at_1, 2)

# a, b 풀이
sol = sp.solve([eq1, eq2], [a, b])
a_val = sol[a]
b_val = sol[b]

result = a_val + b_val

if result == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')