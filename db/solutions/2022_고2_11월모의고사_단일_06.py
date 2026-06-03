import sympy as sp
x = sp.Symbol('x', positive=True)
# 조건을 만족하는 가장 단순한 f(x) = 3x 로 역대입
f_x = 3 * x
expr = (2*x**2 - 1) / (f_x**2 + 3*x**2)
limit_val = sp.limit(expr, x, sp.oo)
expected = sp.Rational(1, 6)
if limit_val == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', limit_val)