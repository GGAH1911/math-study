import sympy as sp
a = sp.pi / 2
x_A = sp.pi / (3 * a)
x_B = 5 * sp.pi / (3 * a)
# 범위 확인
period_end = 2 * sp.pi / a
assert 0 <= x_A <= period_end, 'x_A out of range'
assert 0 <= x_B <= period_end, 'x_B out of range'
# y값 확인
y_A = 2 * sp.cos(a * x_A)
y_B = 2 * sp.cos(a * x_B)
# 거리 확인
AB = sp.simplify(x_B - x_A)
if (sp.simplify(y_A - 1) == 0 and sp.simplify(y_B - 1) == 0 and sp.simplify(AB - sp.Rational(8, 3)) == 0):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
