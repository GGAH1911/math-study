from sympy import *

R2 = Rational(64, 7)
R = sqrt(R2)

# Triangle sides (discriminant check: (b+c)^2 - 4bc = 81R^2/16 - 7R^2/2 = 25R^2/16 > 0)
b = 7*R/4
c = R/2
a = R*sqrt(15)/2

# Verify cos A = -1/4
cosA = (b**2 + c**2 - a**2) / (2*b*c)

# Verify sin B + sin C = 9/8
sinBC = (b + c) / (2*R)

# Verify area = sqrt(15)
area = Rational(1,2)*b*c*(sqrt(15)/4)

# Circumscribed circle area = 64/7 * pi => p=7, q=64, p+q=71
circle_area = pi * R2

pass1 = simplify(cosA + Rational(1,4)) == 0
pass2 = simplify(sinBC - Rational(9,8)) == 0
pass3 = simplify(area - sqrt(15)) == 0
pass4 = (circle_area == Rational(64,7)*pi)

if pass1 and pass2 and pass3 and pass4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print('cosA:', simplify(cosA))
    print('sinB+sinC:', simplify(sinBC))
    print('area:', simplify(area))
    print('circle_area:', circle_area)
