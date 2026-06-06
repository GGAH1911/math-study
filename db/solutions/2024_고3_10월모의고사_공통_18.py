import sympy as sp
c = sp.Rational(4, 3)
S = 16 / c
print('S =', S)
print('Check 1: c*S =', c*S)
print('Check 2: S + 9*c =', S + 9*c)
if c*S == 16 and S + 9*c == 24:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')