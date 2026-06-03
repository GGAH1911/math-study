import sympy as sp
val = (2**(sp.sqrt(2)+1))**(-1) * 2**sp.sqrt(2)
result = sp.simplify(val)
if result == sp.Rational(1, 2):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', result)