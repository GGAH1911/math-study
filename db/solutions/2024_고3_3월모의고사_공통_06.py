from sympy import symbols, solve, Eq

# 등비수열의 첫째항 a1과 공비 r
a1, r = symbols('a1 r', real=True, positive=True)

# 조건 1: S4/S2 = 5
S2 = a1 * (1 + r)
S4 = a1 * (1 + r + r**2 + r**3)
eq1 = Eq(S4 / S2, 5)

# 조건 2: a5 = 48
a5 = a1 * r**4
eq2 = Eq(a5, 48)

# 연립방정식 풀기
sol = solve([eq1, eq2], [a1, r])
print(f'Solutions: {sol}')

# r > 1인 해 선택
valid_sol = [s for s in sol if s[1] > 1][0]
a1_val, r_val = valid_sol
print(f'a1 = {a1_val}, r = {r_val}')

# 검증
S2_check = a1_val * (1 + r_val)
S4_check = a1_val * (1 + r_val + r_val**2 + r_val**3)
a5_check = a1_val * r_val**4
ratio = S4_check / S2_check

print(f'S4/S2 = {ratio} (should be 5)')
print(f'a5 = {a5_check} (should be 48)')

# 최종 답
a1_final = a1_val
a4_final = a1_val * r_val**3
answer = a1_final + a4_final
print(f'a1 + a4 = {answer}')

if ratio == 5 and a5_check == 48:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')