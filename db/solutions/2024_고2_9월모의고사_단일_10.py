from sympy import symbols, solve, simplify

# 등비수열 검증
a = 1
r = 2

# 조건 1: a_2 = 2
a2 = a * r
assert a2 == 2, f'a_2 = {a2}, expected 2'

# 조건 2: S_6 = 9*S_3
S3 = a * (1 + r + r**2)
S6 = a * (1 + r + r**2 + r**3 + r**4 + r**5)
assert S6 == 9 * S3, f'S_6 = {S6}, 9*S_3 = {9*S3}'

# 답: a_4
a4 = a * r**3
assert a4 == 8, f'a_4 = {a4}, expected 8'

print('VERIFY_PASS')