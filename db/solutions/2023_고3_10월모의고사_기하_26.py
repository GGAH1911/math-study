from sympy import *
x_A = Rational(5,4); y_A = Integer(1)
x_B = Integer(5); y_B = Integer(4)
F = (Integer(2), Integer(0))

# 1) A, B가 포물선 y^2=4(x-1) 위에 있는지
assert y_A**2 == 4*(x_A-1), 'A not on parabola'
assert y_B**2 == 4*(x_B-1), 'B not on parabola'

# 2) A, B, O 동선
assert y_A * x_B == y_B * x_A, 'Not collinear with O'

# 3) AF = AH
AF = sqrt((x_A-F[0])**2 + (y_A-F[1])**2)
AH = x_A  # foot of perpendicular to y-axis
assert simplify(AF - AH) == 0, 'AF != AH'

# 4) AF:BF = 1:4
BF = sqrt((x_B-F[0])**2 + (y_B-F[1])**2)
assert simplify(AF/BF - Rational(1,4)) == 0, 'ratio wrong'

# 5) AF = 5/4
assert AF == Rational(5,4), f'AF={AF}, expected 5/4'

print('VERIFY_PASS')
