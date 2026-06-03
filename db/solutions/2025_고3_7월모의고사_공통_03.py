import math

# 주어진 조건을 만족하는 수열 검증
a = 2
r_cubed = 2  # r^3 = 2

# a_1, a_2, a_5, a_13 계산
a1 = a
a2 = a * (2 ** (1/3))  # a * r
a5 = a * (2 ** (4/3))  # a * r^4
a13 = a * (2 ** 4)     # a * r^12
a4 = a * r_cubed       # a * r^3

# 조건 1 확인: a_1 * a_13 = 64
cond1 = abs(a1 * a13 - 64) < 1e-10

# 조건 2 확인: a_5 / a_2 = 2
cond2 = abs(a5 / a2 - 2) < 1e-10

# a_4 값 확인
verify_a4 = abs(a4 - 4) < 1e-10

if cond1 and cond2 and verify_a4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')