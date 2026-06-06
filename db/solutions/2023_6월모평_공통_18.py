import sympy as sp

# 원래 문제: 합이 250이 되어야 함
# a = 3일 때 검증
a = 3

# 합 계산
total = sum(4*k + a for k in range(1, 11))

if total == 250:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')