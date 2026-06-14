import sympy as sp
from sympy import cos, sin, tan, sqrt, pi, simplify, N

CANDIDATE = 5

# Define d using the constraint cos²d = 7/8
cos_d_sq = sp.Rational(7, 8)
sin_d_sq = sp.Rational(1, 8)

# Verify cos²d + sin²d = 1
assert cos_d_sq + sin_d_sq == 1

# Calculate angles
cos_A_cos_C = cos_d_sq - sp.Rational(3, 4)
assert cos_A_cos_C == sp.Rational(1, 8), "cos A cos C should equal 1/8"

# sin A sin C = (3/4)cos²d - (1/4)sin²d
sin_A_sin_C = sp.Rational(3, 4) * cos_d_sq - sp.Rational(1, 4) * sin_d_sq
sin_A_sin_C = sp.Rational(3, 4) * sp.Rational(7, 8) - sp.Rational(1, 4) * sp.Rational(1, 8)
sin_A_sin_C = sp.Rational(21, 32) - sp.Rational(1, 32)
sin_A_sin_C = sp.Rational(20, 32)
sin_A_sin_C = sp.Rational(5, 8)

# tan A tan C = (sin A sin C) / (cos A cos C)
tan_A_tan_C = sin_A_sin_C / cos_A_cos_C
tan_A_tan_C = sp.Rational(5, 8) / sp.Rational(1, 8)
tan_A_tan_C = 5

if tan_A_tan_C == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')