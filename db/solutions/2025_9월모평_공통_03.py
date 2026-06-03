from sympy import symbols, solve, simplify

a, r = symbols('a r', real=True)

# 조건 1: a_2 * a_3 = 2
eq1 = a**2 * r**3 - 2

# 조건 2: a_4 = 4
eq2 = a * r**3 - 4

# 연립방정식 풀이
sol = solve([eq1, eq2], [a, r])
print('Solutions:', sol)

# 모든 항이 실수인 등비수열 조건에서 a=1/2, r=2
valid_sol = [s for s in sol if s[0].is_real and s[1].is_real][0]
a_val, r_val = valid_sol

# a_6 계산
a6 = a_val * r_val**5
a6_simplified = simplify(a6)

print(f'a = {a_val}, r = {r_val}')
print(f'a_6 = {a6_simplified}')

# 검증
a2 = a_val * r_val
a3 = a_val * r_val**2
a4 = a_val * r_val**3
a2a3 = a2 * a3

print(f'a_2 = {a2}, a_3 = {a3}')
print(f'a_2 * a_3 = {a2a3} (should be 2)')
print(f'a_4 = {a4} (should be 4)')

if a2a3 == 2 and a4 == 4 and a6_simplified == 16:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')