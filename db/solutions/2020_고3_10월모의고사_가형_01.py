from sympy import symbols, limit, oo, simplify

n = symbols('n')
expr = n*(9*n - 5) / (3*n**2 + 1)
result = limit(expr, n, oo)

if result == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')