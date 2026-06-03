import math
m = 1/2
n = 1/4
# 첫 번째 조건: log_2(m^2 + 1/4) = -1
lhs1 = math.log2(m**2 + 1/4)
rhs1 = -1
assert abs(lhs1 - rhs1) < 1e-10, f'조건 1 불만족: {lhs1} != {rhs1}'
# 두 번째 조건: log_2(m) = 5 + 3*log_2(n)
lhs2 = math.log2(m)
rhs2 = 5 + 3*math.log2(n)
assert abs(lhs2 - rhs2) < 1e-10, f'조건 2 불만족: {lhs2} != {rhs2}'
# 최종 답
result = m + n
assert abs(result - 0.75) < 1e-10, f'답 오류: {result}'
print('VERIFY_PASS')