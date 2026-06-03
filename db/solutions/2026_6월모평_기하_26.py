from sympy import *
a2 = Integer(12)
b2 = Integer(3)
# 점근선 확인: b/a = 1/2
check_asymptote = simplify(sqrt(b2)/sqrt(a2) - Rational(1, 2)) == 0
# y=1과의 교점
x = symbols('x')
hyperbola_eq = x**2/a2 - Integer(1)/b2 - 1
x_sols = solve(hyperbola_eq, x)
x_P = max(x_sols)
x_Q = min(x_sols)
# 접선 기울기 dy/dx = b^2*x/(a^2*y), y=1
m_P = b2 * x_P / (a2 * 1)
m_Q = b2 * x_Q / (a2 * 1)
# 수직 조건
check_perp = simplify(m_P * m_Q + 1) == 0
if check_asymptote and check_perp:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')