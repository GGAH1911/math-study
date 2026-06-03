from sympy import symbols, expand
x = symbols('x')
lhs = expand((x + 2) * (x**2 - 2*x + 4))
rhs = expand(x**3 + (3 - 3)*x + 4*2)
if lhs == rhs:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')