from sympy import *
x = symbols('x')
f = x**2 - 4*x
g1 = -x**2 + 2*x
g2 = -x**2 + 6*x - 8
# 교점 확인
assert 0 in solve(f - g1, x), 'x=0 not intersection for x<2'
assert 4 in solve(f - g2, x), 'x=4 not intersection for x>=2'
# 넓이 계산
area1 = integrate(g1 - f, (x, 0, 2))
area2 = integrate(g2 - f, (x, 2, 4))
total = area1 + area2
expected = Rational(40, 3)
if total == expected:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {total}, expected {expected}')