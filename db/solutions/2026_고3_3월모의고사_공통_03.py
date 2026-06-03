from sympy import symbols, Eq, solve

# 공차 d를 구함
d = symbols('d')
a1 = 2
a2 = a1 + d
a7 = a1 + 6*d

# 조건식: 2a2 + a7 = 30
eq = Eq(2*a2 + a7, 30)
d_val = solve(eq, d)[0]

# a10 계산
a10 = a1 + 9*d_val

# 검증
print(f'공차 d = {d_val}')
print(f'a10 = {a10}')

# 원래 조건식으로 검증
a2_check = a1 + d_val
a7_check = a1 + 6*d_val
verify = 2*a2_check + a7_check
print(f'2a2 + a7 = {verify} (조건: 30)')

if a10 == 29 and verify == 30:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')