import math

# 구한 답: a = 6, b = 2, k = -1
a, b, k = 6, 2, -1

# 조건 (가): b = log_2(a+2) + k
condition_ga = b == math.log2(a + 2) + k

# 조건 (나): a = 4^(b+k) + 2
condition_na = a == 4**(b + k) + 2

# a != b 확인
a_not_equal_b = a != b

# 모든 조건 확인
if condition_ga and condition_na and a_not_equal_b:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')