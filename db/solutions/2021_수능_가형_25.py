import sympy as sp

# 공차 계산
d = 4
a = lambda k: 3 + (k-1)*d

# 조건 검증: 합 = 55
sum_a = sum(a(k) for k in range(1, 6))
assert sum_a == 55, f"Sum condition failed: {sum_a} != 55"

# 구하는 값
result = sum(k * (a(k) - 3) for k in range(1, 6))

if result == 160:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')