import sympy as sp
from sympy import sqrt, log, symbols, simplify

# 수열의 조건: log_2(a_{n+1}/a_n) = 1/2
# 따라서 a_{n+1}/a_n = sqrt(2)
# a_n = a_1 * (sqrt(2))^(n-1) 형태

# 첫항을 a_1 = 1로 설정 (비율에는 영향 없음)
a_1 = 1
r = sqrt(2)  # 공비

# S_n = a_1 * (r^n - 1) / (r - 1)
S_6 = a_1 * (r**6 - 1) / (r - 1)
S_12 = a_1 * (r**12 - 1) / (r - 1)

# 값 계산
S_6_val = simplify(S_6)
S_12_val = simplify(S_12)

ratio = simplify(S_12_val / S_6_val)

# 검증
if ratio == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Expected: 9, Got: {ratio}')