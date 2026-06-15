from sympy import symbols, diff

x, y = symbols('x y', real=True)
F = x**2 + x*y + y**3 - 7

assert F.subs([(x, 2), (y, 1)]) == 0

dF_dx = diff(F, x)
dF_dy = diff(F, y)
dy_dx = -dF_dx / dF_dy

slope = dy_dx.subs([(x, 2), (y, 1)])

if slope == -1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')