CANDIDATE = 4

# 등차수열 조건
# a_1 + d = 5
# a_1 + 3d = 13

from sympy import symbols, Eq, solve

a1, d = symbols('a1 d')
eq1 = Eq(a1 + d, 5)
eq2 = Eq(a1 + 3*d, 13)

sol = solve([eq1, eq2], [a1, d])
found_d = sol[d]

# 원래 조건들을 만족하는지 확인
a1_val = sol[a1]
print(f'공차: {found_d}')

# 첫 번째 조건 검증
sum1 = a1_val + (a1_val + found_d) + (a1_val + 2*found_d)
print(f'a1+a2+a3 = {sum1} (기대값: 15)')

# 두 번째 조건 검증
sum2 = (a1_val + 2*found_d) + (a1_val + 3*found_d) + (a1_val + 4*found_d)
print(f'a3+a4+a5 = {sum2} (기대값: 39)')

if found_d == CANDIDATE and sum1 == 15 and sum2 == 39:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')