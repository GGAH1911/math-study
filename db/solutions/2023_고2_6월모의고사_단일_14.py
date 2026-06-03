from sympy import sqrt, simplify, Rational
m, n = 12, 32
left_side = ((5**(Rational(1,6))) / (2**(Rational(1,4))))**m * n
right_side = 100
result = simplify(left_side)
if result == right_side:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')