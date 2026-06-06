import math

# 원래 식: log_2(120) - 1/log_15(2)
term1 = math.log(120) / math.log(2)
term2 = 1 / (math.log(2) / math.log(15))
result = term1 - term2

# 검증: term2 = log_2(15) 확인
log2_15 = math.log(15) / math.log(2)
verify_term2 = log2_15

# 최종 계산: log_2(120) - log_2(15) = log_2(120/15) = log_2(8) = 3
final_value = math.log(120/15) / math.log(2)
expected = 3

if abs(result - expected) < 1e-10 and abs(final_value - 3) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')