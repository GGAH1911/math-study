import math

# log는 상용로그(밑 10)
log = math.log10

# 주어진 조건
value_1_44 = 1.44
a = log(value_1_44)

# 검증할 식: 2log 12 = a + 2
computed_2log12 = 2 * log(12)
candidate = a + 2

if math.isclose(computed_2log12, candidate, rel_tol=1e-9):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')