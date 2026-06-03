from sympy import *
a_val = log(6, 2)
x0 = log(3, 2)
y0 = 2**x0 - 1  # on y=2^x-1
y0_check = 2**(-x0 + a_val)  # on y=2^{-x+a}
OB = 2**a_val
OH = y0
cond1 = simplify(y0 - y0_check)  # A on both curves
cond2 = simplify(OB - 3*OH)       # OB = 3*OH
if simplify(cond1) == 0 and simplify(cond2) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', cond1, cond2)
