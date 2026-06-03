from sympy import *
x = symbols('x')
f = (x-1)**2 * (x-3)
result = f.subs(x, 4)
if result == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')