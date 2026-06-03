from sympy import *

# 주어진 조건 검증
sin_t = Rational(3, 5)
cos_t = Rational(-4, 5)
k = Rational(-12, 5)

# 이차방정식 5x^2 + x + k = 0의 근이 sin_t, cos_t인지 확인
eq = 5*sin_t**2 + sin_t + k
print(f'sin_t 대입: {eq}')
assert eq == 0, 'sin_t는 방정식의 근이 아님'

eq = 5*cos_t**2 + cos_t + k
print(f'cos_t 대입: {eq}')
assert eq == 0, 'cos_t는 방정식의 근이 아님'

# 삼각함수 항등식 확인
assert sin_t**2 + cos_t**2 == 1, '삼각함수 항등식 위반'

# tan_t 계산 및 최종 답 계산
tan_t = sin_t / cos_t
result = k * tan_t
print(f'k × tan_t = {result}')
assert result == Rational(9, 5), '최종 답이 다름'

print('VERIFY_PASS')