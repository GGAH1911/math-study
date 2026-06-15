from sympy import symbols, limit
x = symbols('x')
f = 3*x**2 + 2
result = limit(f, x, 1)
if result == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')