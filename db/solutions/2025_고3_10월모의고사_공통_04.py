import sympy as sp
a_val = 6
x = sp.Symbol('x')
f_left = 3**2 + a_val
f_right = 3 + 2*a_val
if f_left == f_right:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')