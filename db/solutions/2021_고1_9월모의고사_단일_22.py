from sympy import symbols, div, expand
x = symbols('x')
P = x**3 + 2*x**2 - x + 2
quotient, remainder = div(P, x - 2, domain='ZZ')
if remainder == 16:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')