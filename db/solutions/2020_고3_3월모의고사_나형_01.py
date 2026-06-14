from sympy import symbols, limit
x = symbols('x')
result = limit(2*x + 5, x, 2)
if result == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')