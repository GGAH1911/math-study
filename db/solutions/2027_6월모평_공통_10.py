import math

# 로그 값 설정
log3_a = 8/3
log3_b = 2/3

# 조건 1 검증: log_9(a) + log_3(b) = 2
cond1 = log3_a / 2 + log3_b
verify1 = math.isclose(cond1, 2)

# 조건 2 검증: log_3(a) = 8*log_9(b)
cond2_left = log3_a
cond2_right = 8 * (log3_b / 2)
verify2 = math.isclose(cond2_left, cond2_right)

# 답 검증
answer = log3_a - log3_b
result = 3 ** answer
verify_answer = math.isclose(result, 9)

if verify1 and verify2 and verify_answer:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')