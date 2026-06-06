from fractions import Fraction
import math

# 등비수열 정의
a1 = Fraction(1, 8)
r = 2

# 일반항
def a_n(n):
    return a1 * (r ** (n - 1))

# 주어진 조건 검증
a2 = a_n(2)
a3 = a_n(3)
ratio = a3 / a2

if ratio == 2:
    # a5 계산
    a5 = a_n(5)
    if a5 == 2:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')