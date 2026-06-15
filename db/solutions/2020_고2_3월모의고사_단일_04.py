from fractions import Fraction

# 두 직선의 기울기
m1 = -2
m2 = Fraction(1, 2)

# 수직 조건 검증
product = m1 * m2

if product == -1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')