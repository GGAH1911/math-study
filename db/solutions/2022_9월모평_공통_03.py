from sympy import symbols, solve, simplify

r = symbols('r', positive=True, real=True)

# 등비수열 조건
a1 = 2
a2 = a1 * r
a4 = a1 * (r**3)
condition = a2 * a4 - 36

# r^4 = 9 구하기
r4_value = solve(condition, r**4)
print(f'r^4 = {r4_value}')

# r^4 = 9 확인
r4 = 9
verify_condition = a1 * r**1 * a1 * r**3 - 36
verify_val = verify_condition.subs(r**4, r4)
print(f'Verification: a2*a4 = {simplify(verify_val.subs(r**4, r4))}')

# 답: a7/a3
a7_over_a3 = r4
print(f'a_7/a_3 = r^4 = {a7_over_a3}')

if a7_over_a3 == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')