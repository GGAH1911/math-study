from sympy import symbols, solve, Eq

x, y = symbols('x y')
eq1 = Eq(x - 2*y, 7)
eq2 = Eq(2*x + y, -1)

solution = solve((eq1, eq2), (x, y))
a, b = solution[x], solution[y]
result = a + b

if result == -2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')