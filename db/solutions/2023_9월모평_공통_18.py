from sympy import symbols, Eq, solve

c = symbols('c')

# 조건 1: 합이 10
sum_a = 10

# 조건 2: sum(c*a_k) = 65 + sum(c)
# 좌변: c * sum(a_k) = c * 10
lhs = c * sum_a

# 우변: 65 + 5*c
rhs = 65 + 5*c

# 방정식
eq = Eq(lhs, rhs)
solution = solve(eq, c)

print(f'Solution: c = {solution[0]}')

# 검증
c_val = solution[0]
lhs_check = c_val * 10
rhs_check = 65 + 5 * c_val

if lhs_check == rhs_check:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')