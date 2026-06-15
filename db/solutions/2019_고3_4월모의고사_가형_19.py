import sympy as sp
from sympy import cos, sin, tan, sec, limit, diff, simplify, pi

theta = sp.Symbol('theta', positive=True, real=True)

# 넓이 함수 정의
S = cos(2*theta) * sin(theta) / (8 * cos(theta)**5)

# 극한값 계산
limit_value = limit(S / theta, theta, 0, '+')
print(f'극한값: {limit_value}')
print(f'수치값: {float(limit_value)}')

# 검증: 답이 1/8인지 확인
if simplify(limit_value - sp.Rational(1, 8)) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')