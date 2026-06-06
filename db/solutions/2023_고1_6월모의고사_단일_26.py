from sympy import symbols, expand
x = symbols('x')
P = x**3 - 2*x**2 - 5*x + 11
remainder = P.subs(x, 4)
print('VERIFY_PASS' if remainder == 23 else 'VERIFY_FAIL')