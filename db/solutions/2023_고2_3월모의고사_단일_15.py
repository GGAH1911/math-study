import sympy as sp
x = sp.Symbol('x')
P = lambda t: t**2 - 3*t - 1
a = 10
lhs = x**3 - x**2 + 3*x - 2
rhs = (x + 2)*P(x) + a*x
equation = sp.expand(lhs - rhs)
if equation == 0:
    result = P(-2)
    print(f'VERIFY_PASS' if result == 9 else f'VERIFY_FAIL')
else:
    print('VERIFY_FAIL')