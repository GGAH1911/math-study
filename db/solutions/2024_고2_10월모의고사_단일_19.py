from sympy import sqrt, pi, Rational, simplify, Integer

AB = Integer(2)
BC = Integer(4)
BD_sq = Integer(6)
BD = sqrt(BD_sq)

# Angle bisector => AD/DC = AB/BC = 1/2, AC=3
AC = Integer(3)
AD = Integer(1)
DC = Integer(2)

# Verify angle bisector ratio
assert Rational(AD, DC) == Rational(AB, BC), 'Bisector ratio fail'

# Verify Stewart's theorem: AB^2*DC + BC^2*AD - BD^2*AC = AC*AD*DC
stewart_lhs = AB**2 * DC + BC**2 * AD - BD_sq * AC
stewart_rhs = AC * AD * DC
assert simplify(stewart_lhs - stewart_rhs) == 0, 'Stewart fail'

# Verify BD = sqrt(6) via coordinates
# B=(0,0), C=(4,0), cos(B)=11/16, A=(11/8, 3*sqrt(15)/8)
# D = (2/3)*A + (1/3)*C = (9/4, sqrt(15)/4)
from sympy import sqrt as Sqrt
BD_check = Sqrt(Rational(9,4)**2 + (Sqrt(15)/4)**2)
assert simplify(BD_check - Sqrt(6)) == 0, 'BD coordinate check fail'

# E: second intersection of circle with BC (y=0)
# Circle: x^2+y^2-(5/2)x-(sqrt(15)/10)y=0 => x=0 or x=5/2
# CE = DC*AC/BC (power of a point)
CE = Rational(DC * AC, BC)  # = 6/4 = 3/2
assert CE == Rational(3, 2), 'CE fail'
assert 0 < CE < BC, 'E not on segment BC'

# DE chord = 1 (equal to AD chord)
# E=(5/2,0), D=(9/4, sqrt(15)/4)
DE_sq = (Rational(5,2) - Rational(9,4))**2 + (Sqrt(15)/4)**2
assert simplify(DE_sq - 1) == 0, 'DE=1 fail'

# Circumradius R of circle through A,B,D
cos_A = Rational(AB**2 + AD**2 - BD_sq, 2 * AB * AD)  # = -1/4
assert cos_A == Rational(-1, 4)
sin_A_sq = 1 - cos_A**2  # = 15/16
R_sq = Rational(BD_sq, 1) / (4 * sin_A_sq)  # BD^2/(4*sin^2)
R_sq = simplify(R_sq)

area = pi * R_sq
expected = Rational(8, 5) * pi

if simplify(area - expected) == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: area={area}, expected={expected}')
