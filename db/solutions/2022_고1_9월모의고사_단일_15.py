from fractions import Fraction

# 주어진 조건
# PQ의 중점이 (4, 5)
# P = 2A, Q = 2B
# PQ의 중점 = (P+Q)/2 = (2A+2B)/2 = A+B

# A+B = (4, 5)
sum_coords = (4, 5)

# 무게중심 G = (O+A+B)/3 = (A+B)/3 = (4/3, 5/3)
a = Fraction(4, 3)
b = Fraction(5, 3)

# a + b 계산
answer = a + b

if answer == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')