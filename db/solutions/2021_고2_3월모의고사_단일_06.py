from sympy import symbols, solve, simplify
a, b = symbols('a b', real=True)
eq1 = a - b - 2
eq2 = a*b - 1/3
sols = solve([eq1, eq2], [a, b])
for sol in sols:
    a_val, b_val = sol
    result = a_val**3 - b_val**3
    expected = 10
    if abs(result - expected) < 1e-9:
        print('VERIFY_PASS')
        break
else:
    print('VERIFY_FAIL')