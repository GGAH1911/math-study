import sympy as sp
a = 4 * sp.sqrt(2)
b = 4 * sp.sqrt(2)
area = sp.Rational(1, 2) * a * b
AB_squared = a**2 + b**2
if area == 16 and AB_squared == 64:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')