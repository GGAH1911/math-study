from sympy import symbols, poly
x = symbols('x')
a = 15
P = x**3 - 2*x**2 - 8*x + a
remainder = P.subs(x, 3)
if remainder == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')