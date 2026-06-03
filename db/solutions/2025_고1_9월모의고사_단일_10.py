from sympy import symbols, Eq, solve
x, y = symbols('x y')
eq1 = Eq(2*x - y, 4)
eq2 = Eq(3*x**2 - x*y - 7*y, 3)
sol = solve([eq1, eq2], [x, y])
results = []
for s in sol:
    alpha, beta = s
    check1 = 2*alpha - beta == 4
    check2 = 3*alpha**2 - alpha*beta - 7*beta == 3
    if check1 and check2:
        results.append(alpha + beta)
if all(v == 11 for v in results) and len(results) > 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', results)
