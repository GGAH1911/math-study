from sympy import symbols, ln, limit
x = symbols('x')
expr = ln(1 + 8*x) / (2*x)
result = limit(expr, x, 0)
if result == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')