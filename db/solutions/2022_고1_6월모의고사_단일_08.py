from sympy import symbols, expand
x = symbols('x')
Q = lambda t: t**2 - 4*t - 2
a = 2
lhs = x**3 - 5*x**2 + a*x + 1
rhs = (x - 1) * Q(x) - 1
if expand(lhs - rhs) == 0:
    result = Q(a)
    print('VERIFY_PASS' if result == -6 else 'VERIFY_FAIL')
else:
    print('VERIFY_FAIL')