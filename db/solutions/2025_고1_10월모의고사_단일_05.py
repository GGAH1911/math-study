from sympy import symbols, solve

# 평행이동 벡터 (p, q) 구하기
# (3, a) -> (8, 8)
p = 8 - 3  # p = 5

# (5, 5) -> (b, 2)
# 5 + p = b
b = 5 + p  # b = 10

# 5 + q = 2
q = 2 - 5  # q = -3

# a 구하기
# a + q = 8
a = 8 - q  # a = 8 - (-3) = 11

# 검증
verify1 = (3 + p == 8 and a + q == 8)
verify2 = (5 + p == b and 5 + q == 2)
result = a + b

if verify1 and verify2 and result == 21:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')