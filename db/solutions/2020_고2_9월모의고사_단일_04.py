import sympy as sp

val = sp.cos(sp.Rational(2, 3) * sp.pi)
expected = sp.Rational(-1, 2)

if val == expected:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {val}, expected {expected}')