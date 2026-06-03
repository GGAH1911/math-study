from fractions import Fraction

# 원래 문제의 일반항
def a_n(n):
    return Fraction(1, (3*n - 2) * (3*n + 1))

# 합 계산
total = sum(a_n(k) for k in range(1, 9))

# 답 검증
answer = Fraction(8, 25)

if total == answer:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')