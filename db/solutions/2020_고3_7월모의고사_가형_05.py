import sympy as sp
a = 4
b = sp.Rational(1, 2)
min_val = a * (-1) + 3
period = 2 * sp.pi / b
result = a + b
if min_val == -1 and period == 4*sp.pi and result == sp.Rational(9, 2):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')