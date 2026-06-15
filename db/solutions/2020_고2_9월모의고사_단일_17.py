from sympy import symbols, solve, summation

# 공차와 첫째항 정의
a = 73  # a_1
d = -6  # 공차

# a_n = a + (n-1)d
def a_n(n):
    return a + (n - 1) * d

# 조건 (가) 검증: a_7 = 37
assert a_n(7) == 37, f"a_7 = {a_n(7)}, expected 37"

# 조건 (나) 검증: a_13 >= 0, a_14 <= 0
assert a_n(13) >= 0, f"a_13 = {a_n(13)}, expected >= 0"
assert a_n(14) <= 0, f"a_14 = {a_n(14)}, expected <= 0"

# 합 계산
total_sum = sum(abs(a_n(k)) for k in range(1, 22))

if total_sum == 689:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')