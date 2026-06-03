from fractions import Fraction

# 공비 r 계산
a1 = Fraction(1, 4)
# a2 + a3 = 3/2
# (1/4)r + (1/4)r^2 = 3/2
# r + r^2 = 6
# r^2 + r - 6 = 0
# (r+3)(r-2) = 0
r = 2  # 양수 조건

# 조건 검증
a2 = a1 * r
a3 = a1 * (r ** 2)
assert a1 == Fraction(1, 4), 'a1 검증 실패'
assert a2 + a3 == Fraction(3, 2), f'a2 + a3 = {a2 + a3} 검증 실패'

# 모든 항이 양수 확인
for n in range(1, 8):
    an = a1 * (r ** (n - 1))
    assert an > 0, f'a{n} 양수 조건 실패'

# a6 + a7 계산 및 검증
a6 = a1 * (r ** 5)
a7 = a1 * (r ** 6)
result = a6 + a7

if result == 24:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')