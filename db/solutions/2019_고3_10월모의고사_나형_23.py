from sympy import log, symbols, simplify, N
import math

CANDIDATE = 4

# a를 임의의 양수(1이 아님)로 설정, 예: a = 2
a_val = 2
b_val = a_val**3  # log_a(b) = 3이므로 b = a^3

# 상용로그(밑 10)
log_b_over_a = math.log10(b_val) - math.log10(a_val)  # log(b/a)
log_a_100 = math.log(100) / math.log(a_val)  # log_a(100)

result = log_b_over_a * log_a_100

if abs(result - CANDIDATE) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')