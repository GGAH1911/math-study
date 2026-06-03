from sympy import Rational, Abs
k = Rational(9, 4)
px, py = -k, k*(4-k)
qx, qy = Rational(-2), Rational(0)
ox, oy = Rational(0), Rational(0)
rx, ry = Rational(0), Rational(1)
# Shoelace
area = Rational(1,2)*Abs((px*qy - qx*py) + (qx*oy - ox*qy) + (ox*ry - rx*oy) + (rx*py - px*ry))
expected = Rational(81, 16)
print('VERIFY_PASS' if area == expected else f'VERIFY_FAIL area={area}')
