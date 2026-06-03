import sympy as sp
a = sp.Symbol('a')

# x=2에서의 연속조건
left_limit = (5 - 2*a)**2  # (2^2 - 2a + 1)^2
right_limit = 1  # (-2 + 1)^2

# 연속 조건 방정식
eq = sp.Eq(left_limit, right_limit)
solutions = sp.solve(eq, a)
print(f'Solutions: {solutions}')

# 각 해가 조건을 만족하는지 확인
for sol in solutions:
    check = (5 - 2*sol)**2
    print(f'a={sol}: (5-2a)^2 = {check}')

# 합 계산
sum_a = sum(solutions)
print(f'Sum of all a: {sum_a}')

if sum_a == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')