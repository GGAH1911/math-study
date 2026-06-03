import sympy as sp
a1, a2 = 6, sp.Rational(1, 5)
d1, d2 = sp.Rational(-3, 2), sp.Rational(-1, 10)

# Case 1
S3_1 = 3*a1 + 3*d1
S6_1 = 6*a1 + 15*d1
S11_1 = 11*a1 + 55*d1
assert abs(S3_1) == abs(S6_1) and abs(S6_1) == abs(S11_1) - 3, 'Case 1 failed'

# Case 2
S3_2 = 3*a2 + 3*d2
S6_2 = 6*a2 + 15*d2
S11_2 = 11*a2 + 55*d2
assert abs(S3_2) == abs(S6_2) and abs(S6_2) == abs(S11_2) - 3, 'Case 2 failed'

result = a1 + a2
assert result == sp.Rational(31, 5), f'Sum mismatch: {result}'
print('VERIFY_PASS')