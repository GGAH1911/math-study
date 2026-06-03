from sympy import *
x = symbols('x')
m_val = 3
f = x**2 + 1
total_area = integrate(f, (x, 0, 1))
assert total_area == Rational(4, 3)
x0 = 1 - Rational(2, m_val)
line = m_val*(x - 1) + 2
curve_minus_line = f - line
roots = solve(curve_minus_line, x)
assert all(r <= 0 or r >= 1 for r in roots if r.is_real and 0 < r < 1), 'Line above curve inside region'
below_area = integrate(line, (x, x0, 1))
above_area = total_area - below_area
if below_area == above_area == total_area / 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
