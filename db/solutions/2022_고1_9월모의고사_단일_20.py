from sympy import symbols, expand
x = symbols('x')
f = lambda t: t**4 - 3*t**3 - 7*t**2 + 9*t + 5
result = f(4)
if result == -7:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')