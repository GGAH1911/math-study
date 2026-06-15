import math

CANDIDATE = 80

# 조건 (가): log₂(log₄ a) = 1
a = 4**2
log4_a = math.log(a, 4)
log2_log4_a = math.log(log4_a, 2)
assert abs(log2_log4_a - 1.0) < 1e-10, f"조건 (가) 실패: {log2_log4_a}"

# 조건 (나): log_a 5 × log₅ b = 3/2
# log₅ b = (3/2) × log₅ a
log5_a = math.log(a, 5)
log5_b = 1.5 * log5_a
b = 5 ** log5_b

# 검증
loga_5 = math.log(5, a)
log5_b_check = math.log(b, 5)
product = loga_5 * log5_b_check
assert abs(product - 1.5) < 1e-10, f"조건 (나) 실패: {product}"

# 최종 검증
result = a + b
assert abs(result - CANDIDATE) < 1e-6, f"답 오류: {result} != {CANDIDATE}"
print('VERIFY_PASS')