import sympy as sp
x, y = sp.symbols('x y')
eq1 = x**2 - 4*x*y + 4*y**2
eq2 = x**2 - 6*x - 12*y + 36
val1 = eq1.subs([(x, 6), (y, 3)])
val2 = eq2.subs([(x, 6), (y, 3)])
if val1 == 0 and val2 == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')