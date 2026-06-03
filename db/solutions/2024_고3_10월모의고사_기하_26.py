from sympy import *

# Parabola y^2 = 12x, focus F=(3,0), p=3
# AF:BF = 3:1

# Focal chord property: 1/AF + 1/BF = 1/p = 1/3
AF_val = Rational(12)
BF_val = Rational(4)

# Check focal chord property
assert Rational(1, AF_val) + Rational(1, BF_val) == Rational(1, 3), 'Focal chord property FAIL'

# Point A
x1 = AF_val - 3  # = 9
y1 = sqrt(12 * x1)  # = 6*sqrt(3), positive for positive slope

# Verify A is on parabola y^2 = 12x
assert simplify(y1**2 - 12*x1) == 0, 'A not on parabola'

# Verify slope is positive: line through F(3,0) and A(9, 6sqrt3)
slope = (y1 - 0) / (x1 - 3)
assert simplify(slope) > 0, 'Slope not positive'

# Tangent at A(x1,y1) on y^2=12x: y*y1 = 6*(x + x1)
# y-intercept: set x=0 -> y = 6*x1/y1
y_intercept = 6 * x1 / y1
y_intercept_simplified = simplify(y_intercept)

expected = 3 * sqrt(3)
if simplify(y_intercept_simplified - expected) == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {y_intercept_simplified}, expected {expected}')
