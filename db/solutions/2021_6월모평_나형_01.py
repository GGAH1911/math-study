import sympy as sp
result = sp.Rational(8)**sp.Rational(1,3) * sp.Rational(4)**sp.Rational(3,2)
if result == 16:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')