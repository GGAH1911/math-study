import math
from fractions import Fraction

# 주어진 $a_1 = -31/2$
a1 = Fraction(-31, 2)
common_diff = 3

# a_n = a_1 + (n-1)*d
def a(n):
    return a1 + (n - 1) * common_diff

# 조건 (가) 검증: a_5 * a_7 < 0
a5 = a(5)
a7 = a(7)
condition_a = a5 * a7 < 0

# 조건 (나) 검증
left_side = sum(abs(a(k + 6)) for k in range(1, 7))
right_side = 6 + sum(abs(a(2 * k)) for k in range(1, 7))
condition_b = (left_side == right_side)

# a_10 계산
a10 = a(10)

if condition_a and condition_b and a10 == Fraction(23, 2):
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: condition_a={condition_a}, condition_b={condition_b} (left={left_side}, right={right_side}), a10={a10}')