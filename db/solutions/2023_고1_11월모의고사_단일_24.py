from sympy import symbols, solve, Eq
x, y = symbols('x y')
eq1 = Eq(x - y, 3)
eq2 = Eq(x**2 - 3*x*y + 2*y**2, 6)
sols = solve([eq1, eq2], [x, y])
print(f'Solutions: {sols}')
alpha, beta = 4, 1
result1 = alpha - beta
result2 = alpha**2 - 3*alpha*beta + 2*beta**2
if result1 == 3 and result2 == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')