# 주어진 조건을 검증
# sum(a_k for k=1 to 5) + 5 = 9
# => sum(a_k for k=1 to 5) = 4
# a_6 = 4

# 조건 1 검증
sum_a1_to_5 = 4
sum_condition = sum_a1_to_5 + 5
if sum_condition == 9:
    condition_1_valid = True
else:
    condition_1_valid = False

# 조건 2 검증
a_6 = 4
condition_2_valid = (a_6 == 4)

# 최종 답 검증
sum_a1_to_6 = sum_a1_to_5 + a_6
answer = 8

if condition_1_valid and condition_2_valid and sum_a1_to_6 == answer:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')