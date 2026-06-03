from sympy import *

# Answer: b^2/a^2 = 7/32
# Concrete values: a^2=32, b^2=7, c^2=25
a2 = Rational(32)
b2 = Rational(7)
c2 = a2 - b2  # 25
c_val = sqrt(c2)  # 5

# Points
F  = (c_val, Integer(0))
Fp = (-c_val, Integer(0))  # F'
Q  = (Integer(0), c_val)   # circle meets y-axis at positive y

# P: circle meets ellipse in first quadrant
yP = b2 / c_val
xP = sqrt(c2**2 - b2**2) / c_val

# Verify P on circle x^2+y^2=c^2
assert simplify(xP**2 + yP**2 - c2) == 0, 'P not on circle'

# Verify P on ellipse x^2/a^2 + y^2/b^2 = 1
assert simplify(xP**2/a2 + yP**2/b2 - 1) == 0, 'P not on ellipse'

# P in first quadrant
assert xP > 0 and yP > 0, 'P not in first quadrant'

# Slopes
m1 = simplify((yP - Fp[1]) / (xP - Fp[0]))  # slope of F'P
m2 = simplify((F[1] - Q[1]) / (F[0] - Q[0]))  # slope of QF

# tan(theta) for the acute angle between two lines
tan_theta = simplify(Abs((m1 - m2) / (1 + m1*m2)))

# cos(theta)
cos_theta = simplify(1 / sqrt(1 + tan_theta**2))

if simplify(cos_theta - Rational(3, 5)) == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: cos_theta = {cos_theta}')
