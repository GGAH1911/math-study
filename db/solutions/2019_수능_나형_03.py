from sympy import symbols, limit, oo

n = symbols('n')
expr = (6*n**2 - 3) / (2*n**2 + 5*n)
result = limit(expr, n, oo)

if result == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')