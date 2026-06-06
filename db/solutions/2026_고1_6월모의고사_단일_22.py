from sympy import symbols, expand, solve
x, a, b = symbols('x a b')
lhs = (x + 3) * (x + 2)
rhs = x**2 + 5*x + 6
result = expand(lhs) - rhs
if result == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')