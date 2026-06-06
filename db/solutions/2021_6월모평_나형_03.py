# 등차수열의 정의: a_n = a_1 + (n-1)*d
# 주어진 조건: a_1 + a_3 = 20
# 답: a_2 = 10

# a_2 = 10일 때, a_1 + d = 10
# a_1 = 10 - d로 놓으면
# a_3 = a_1 + 2d = (10 - d) + 2d = 10 + d
# a_1 + a_3 = (10 - d) + (10 + d) = 20 ✓

# 임의의 d값으로 검증 (예: d=3)
d = 3
a_1 = 10 - d  # a_1 = 7
a_2 = a_1 + d  # a_2 = 10
a_3 = a_1 + 2*d  # a_3 = 13

result = a_1 + a_3
expected = 20
assert result == expected, f'a_1 + a_3 = {result}, expected {expected}'
assert a_2 == 10, f'a_2 = {a_2}, expected 10'

print('VERIFY_PASS')