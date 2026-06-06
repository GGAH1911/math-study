import sympy as sp
x = sp.Symbol('x')
a, b, c = -7, 1, 2
lhs = 3*x**2 + a*x + 4
rhs = b*x*(x-1) + c*(x-1)*(x-2)
diff = sp.expand(lhs - rhs)
if diff == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')