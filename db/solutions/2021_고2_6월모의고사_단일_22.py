import sympy as sp
result = 5**(sp.Rational(7,3)) / 5**(sp.Rational(1,3))
expected = 25
if abs(float(result) - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')