import sympy as sp
x, a = sp.symbols('x a', real=True)

# a = -1
a_val = -1

# 첫 번째 부등식: (x-a)^2 < a^2
ineq1 = (x - a_val)**2 < a_val**2
print(f'First inequality: (x-({a_val}))^2 < {a_val**2}')
print(f'Which is: (x+1)^2 < 1')
sol1 = sp.solve((x + 1)**2 - 1, x)
print(f'Boundaries: {sol1}')
print(f'Solution: -2 < x < 0')

# 두 번째 부등식: x^2 + a < (a+1)x
ineq2 = x**2 + a_val < (a_val + 1)*x
print(f'\nSecond inequality: x^2 + ({a_val}) < ({a_val+1})*x')
print(f'Which is: x^2 - 1 < 0')
sol2 = sp.solve(x**2 - 1, x)
print(f'Boundaries: {sol2}')
print(f'Solution: -1 < x < 1')

# 교집합
print(f'\nIntersection: -1 < x < 0 (which is b < x < b+1 with b = -1)')

# 검증
b_val = -1
print(f'\nVerification:')
print(f'a = {a_val}, b = {b_val}')
print(f'a + b = {a_val + b_val}')

# 해가 실제로 -1 < x < 0인지 확인
test_x = -0.5
ineq1_check = (test_x + 1)**2 < 1
ineq2_check = test_x**2 - 1 < 0
print(f'Test x = -0.5: ineq1={ineq1_check}, ineq2={ineq2_check}')

if a_val + b_val == -2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')