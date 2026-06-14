from sympy import symbols, solve, Eq

# 등차수열: a_n = a_1 + (n-1)*d
# 조건: a_2 = 5, a_5 = 11

a1, d = symbols('a1 d')
eq1 = Eq(a1 + d, 5)
eq2 = Eq(a1 + 4*d, 11)

sol = solve([eq1, eq2], [a1, d])
print(f'a1 = {sol[a1]}, d = {sol[d]}')

a1_val = sol[a1]
d_val = sol[d]

# a_8 계산
a8 = a1_val + 7 * d_val
print(f'a_8 = {a8}')

# 검증
a2_check = a1_val + d_val
a5_check = a1_val + 4 * d_val
print(f'a_2 검증: {a2_check} (기대: 5)')
print(f'a_5 검증: {a5_check} (기대: 11)')

if a2_check == 5 and a5_check == 11 and a8 == 17:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')