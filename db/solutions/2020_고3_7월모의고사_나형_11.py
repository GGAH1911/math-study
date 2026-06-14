from sympy import sqrt, simplify, Rational

# sin(theta) + cos(theta) = 1/2, sin(theta)*cos(theta) = -3/8 만족하는 값
sin_theta = (1 + sqrt(7)) / 4
cos_theta = (1 - sqrt(7)) / 4

# 조건 검증
assert simplify(sin_theta + cos_theta) == Rational(1, 2)
assert simplify(sin_theta * cos_theta) == Rational(-3, 8)

# 핵심 계산: (sin + cos) / (sin * cos)
result = simplify((sin_theta + cos_theta) / (sin_theta * cos_theta))

if result == Rational(-4, 3):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')