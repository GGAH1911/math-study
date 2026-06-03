import math

# 답: a_11 = 96
# 구한 값: a = 3, r = sqrt(2)
a = 3
r = math.sqrt(2)

# 검증 1: a_3 * a_8 / a_6 = 12
a_3 = a * (r ** 2)
a_8 = a * (r ** 7)
a_6 = a * (r ** 5)
result1 = (a_3 * a_8) / a_6

# 검증 2: a_5 + a_7 = 36
a_5 = a * (r ** 4)
a_7 = a * (r ** 6)
result2 = a_5 + a_7

# 검증 3: a_11 = 96
a_11 = a * (r ** 10)

if abs(result1 - 12) < 1e-10 and abs(result2 - 36) < 1e-10 and abs(a_11 - 96) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')