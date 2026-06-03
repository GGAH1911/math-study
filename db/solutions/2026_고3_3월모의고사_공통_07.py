from sympy import symbols, integrate, Rational
x = symbols('x')
f = x**2        # 포물선 (위)
g = x - 2       # 직선 (아래)
# 구간 [0,2]에서 f >= g 확인
diff_fn = f - g
checks = [diff_fn.subs(x, v) for v in [0, 1, 2]]
assert all(v >= 0 for v in checks), 'VERIFY_FAIL: 대소 관계 오류'
# 넓이 계산
area = integrate(diff_fn, (x, 0, 2))
expected = Rational(14, 3)
if area == expected:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {area}, expected {expected}')
