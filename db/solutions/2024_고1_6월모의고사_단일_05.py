from sympy import symbols, expand
x = symbols('x')
a, b = 1, 3
lhs = 2*x**2 + a*x + b
rhs = x*(x-3) + (x+1)*(x+3)
rhs_expanded = expand(rhs)
lhs_expanded = expand(lhs)
if lhs_expanded == rhs_expanded:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')