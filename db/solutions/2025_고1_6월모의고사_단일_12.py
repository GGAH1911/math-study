from sympy import symbols, expand, simplify
x = symbols('x')
P = x**4 - 2*x**3 - 12*x**2 + 45*x - 41
result = P.subs(x, 3)
if result == 13:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')