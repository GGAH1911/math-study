from sympy import symbols, Eq, solve, Rational

a_val = Rational(5, 2)
x, y = symbols('x y')

eq1 = Eq(a_val*x + 4*y, 12)
eq2 = Eq(2*x + a_val*y, a_val + 5)

sol = solve([eq1, eq2], [x, y])

if sol[x] == 0 and sol[y] == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
