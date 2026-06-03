import sympy as sp
from sympy import E, exp, diff, symbols, simplify, Abs

# x > 0에서 곡선 y = e^x
x = symbols('x', real=True)
y = exp(x)
dy_dx = diff(y, x)  # e^x

# 원점을 지나는 접선: 점 (a, e^a)에서
# y - e^a = e^a(x - a) → 0 - e^a = e^a(0 - a)
# a = 1

a_val = 1
slope = dy_dx.subs(x, a_val)  # e

# 대칭성에 의해 두 접선의 기울기
m1 = E
m2 = -E

# 두 직선의 교각
tan_theta = Abs((m1 - m2) / (1 + m1 * m2))
tan_theta_simplified = simplify(tan_theta)  # 2e/(e^2-1)

expected = 2 * E / (E**2 - 1)
expected_simplified = simplify(expected)

if simplify(tan_theta_simplified - expected_simplified) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')