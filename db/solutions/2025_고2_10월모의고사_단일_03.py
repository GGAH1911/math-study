import sympy as sp

# 등비수열 a, 4, b에서 공비를 r이라 하면
# 4 = a*r, b = 4*r
# 따라서 a*b = (4/r) * (4*r) = 16

# 검증: 등비수열 성질 - 중간항의 제곱 = 양쪽 항의 곱
middle_term = 4
product = 16

# 중간항의 제곱
middle_squared = middle_term ** 2

if middle_squared == product:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')