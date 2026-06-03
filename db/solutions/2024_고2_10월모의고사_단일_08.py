from fractions import Fraction

# 부분합 공식
def S(n):
    return Fraction(1, n+1)

# a_1 계산
a1 = S(1)

# a_5 계산 (n >= 2일 때 a_n = S_n - S_{n-1})
a5 = S(5) - S(4)

# a_1 + a_5
result = a1 + a5

# 검증: result = 7/15
if result == Fraction(7, 15):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')