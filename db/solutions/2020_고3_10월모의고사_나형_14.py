from sympy import *

CANDIDATE = Rational(20, 3)

# 등차수열 설정
d = Rational(5, 3)
a5 = 5
a1 = a5 - 4*d

# 항들 계산
a3 = a1 + 2*d
a4 = a1 + 3*d
a5_check = a1 + 4*d
a6 = a1 + 5*d
a7 = a1 + 6*d

# 검증 1: a5 = 5인지 확인
assert a5_check == 5, f"a5 should be 5, got {a5_check}"

# 검증 2: 공차가 양수인지 확인
assert d > 0, f"d should be positive, got {d}"

# 검증 3: 합 조건 확인
sum_abs = abs(2*a3 - 10) + abs(2*a4 - 10) + abs(2*a5_check - 10) + abs(2*a6 - 10) + abs(2*a7 - 10)
assert sum_abs == 20, f"Sum should be 20, got {sum_abs}"

# 검증 4: a6 계산 확인
assert a6 == CANDIDATE, f"a6 should be {CANDIDATE}, got {a6}"

print('VERIFY_PASS')