# 검증: 주어진 조건을 만족하는지 확인
# S_ab = sum(a_n * b_n), S_a_plus_b = sum(a_n + b_n), S_a_plus_b = 44
# 조건 1: sum((a_n - 2)(b_n - 2)) = 60
# 전개하면: S_ab - 2*sum(a_n) - 2*sum(b_n) + 28 = 60
#         = S_ab - 2*(sum(a_n) + sum(b_n)) + 28 = 60
#         = S_ab - 2*S_a_plus_b + 28 = 60

S_a_plus_b = 44
S_ab = 120

# 조건 1 검증
condition_1 = S_ab - 2 * S_a_plus_b + 28
expected_1 = 60

if condition_1 == expected_1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')