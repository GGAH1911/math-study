from sympy import symbols, expand
x = symbols('x')
lhs = (x+2)*(x+3)*(x+4)*(x+5) + 1
rhs = (x**2 + 7*x + 11)**2
if expand(lhs) == expand(rhs):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')