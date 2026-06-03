import sympy as sp
x, y = sp.symbols('x y', real=True, positive=True)
eq1 = 2*x**2 - 5*x*y + 2*y**2
eq2 = 4*x**2 - y**2 - 45
alpha, beta = 2*sp.sqrt(3), sp.sqrt(3)
check1 = eq1.subs([(x, alpha), (y, beta)])
check2 = eq2.subs([(x, alpha), (y, beta)])
if check1 == 0 and check2 == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')