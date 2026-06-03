from sympy import symbols, expand, div
x = symbols('x')
P = 2*x**3 - x**2 - x + 4
remainder = P.subs(x, 1)
if remainder == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')