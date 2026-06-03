import sympy as sp
from sympy import log

x1, x2 = sp.Rational(1, 9), 3

def verify_root(x_val):
    if 0 < x_val <= 1:
        f_x = log(x_val, sp.Rational(1, 3))
    else:
        f_x = log(x_val, 3)
    
    if 0 < 3*x_val <= 1:
        f_3x = log(3*x_val, sp.Rational(1, 3))
    else:
        f_3x = log(3*x_val, 3)
    
    result = f_x + f_3x
    return sp.simplify(result) == 3

if verify_root(x1) and verify_root(x2):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')