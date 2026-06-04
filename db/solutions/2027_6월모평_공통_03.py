from sympy import symbols, Eq, solve

A, B = symbols('A B')
eq1 = Eq(2*A + B, 19)
eq2 = Eq(A + B, 10)

sol = solve([eq1, eq2], [A, B])
result = sol[A]

if result == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')