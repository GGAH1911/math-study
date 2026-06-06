import math

# 조건: a_1 = 1/4, 공비 r > 0
# a_3 + a_5 = 1/a_3 + 1/a_5
# 이를 정리하면 a_3 * a_5 = 1
# (1/4 * r^2) * (1/4 * r^4) = 1
# r^6 = 16
# r = 16^(1/6)

r = 16 ** (1/6)
a_1 = 1/4

# a_n = a_1 * r^(n-1)
a_3 = a_1 * (r ** 2)
a_5 = a_1 * (r ** 4)

# 원래 조건 검증
lhs = a_3 + a_5
rhs = 1/a_3 + 1/a_5
condition_satisfied = abs(lhs - rhs) < 1e-10

# 답 검증
a_10 = a_1 * (r ** 9)
answer = 16
answer_correct = abs(a_10 - answer) < 1e-10

if condition_satisfied and answer_correct:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')