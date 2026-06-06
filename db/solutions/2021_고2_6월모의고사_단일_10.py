import sympy as sp

a, b, c = sp.Rational(3), sp.Rational(1,2), sp.Rational(2)

# 원래 함수
def f(x):
    return a * sp.tan(b * x) + c

# 검증 1: y-절편 = 2
assert f(0) == 2, f'y-intercept {f(0)} != 2'

# 검증 2: x=pi/2 에서 y=5
assert f(sp.pi/2) == 5, f'f(pi/2) = {f(sp.pi/2)} != 5'

# 검증 3: 점근선이 x = -pi, pi, 3pi 인지 확인
# b*x = pi/2 + n*pi => x = (2n+1)*pi  (b=1/2)
for n in [-1, 0, 1]:
    expected = (2*n+1)*sp.pi
    actual = (sp.pi/2 + n*sp.pi) / b
    assert sp.simplify(expected - actual) == 0, f'asymptote mismatch n={n}'

# 검증 4: 모두 양수
assert a > 0 and b > 0 and c > 0

# 최종 값
result = a * b * c
if result == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
