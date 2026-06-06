import math

# 원래 문제의 조건
a, b, c = 8, 16, 32

# 조건 1: a + b = 24
cond1 = (a + b == 24)

# 조건 2: B의 모든 원소의 합 = 12
log_sum = math.log2(a) + math.log2(b) + math.log2(c)
cond2 = (abs(log_sum - 12.0) < 1e-9)

# 조건 3: a, b, c는 서로 다른 자연수
cond3 = (len({a, b, c}) == 3 and all(x > 0 and isinstance(x, int) for x in [a, b, c]))

# 원래 식 검증: log_2(abc) = 12 => abc = 4096
abc_product = a * b * c
cond4 = (abc_product == 4096)

if cond1 and cond2 and cond3 and cond4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')