from fractions import Fraction

a = 9
b = 8

# 조건 1: 도수 합
total = 7 + 11 + a + 10 + b
assert total == 45, f'합계 오류: {total}'

# 조건 2: a + b = 17
assert a + b == 17, f'a + b 오류'

# 조건 3: 상대도수가 유한소수 (분모가 2^m * 5^n 형태)
rel_freq = Fraction(a, 45)
den = rel_freq.denominator

# 분모가 2와 5의 곱인지 확인
temp = den
while temp % 2 == 0:
    temp //= 2
while temp % 5 == 0:
    temp //= 5

is_finite_decimal = (temp == 1) and (a > 0)
assert is_finite_decimal, f'유한소수 조건 미충족'

# 답 검증
result = 2 * a + b
assert result == 26, f'답 오류: {result}'

print('VERIFY_PASS')