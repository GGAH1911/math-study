from sympy import *
k = 2
alpha = atan(Rational(1, 2))
sa, ca = sin(alpha), cos(alpha)  # 1/sqrt(5), 2/sqrt(5)

# Points
xA, yA = alpha, ca
xB, yB = pi + alpha, -ca

# External division 3:1
xC = (3*xB - xA) / 2
yC = (3*yB - yA) / 2

# Verify C on f(x) = 2*sin(x)
assert simplify(k*sin(xC) - yC) == 0, 'C not on f(x)'

# D on g(x) = cos(x)
xD = xC
yD = cos(xD)

# Triangle BCD area
CD = simplify(abs(yD - yC))
h = simplify(xC - xB)
area = Rational(1,2) * CD * h

expected = sqrt(5)*pi/4
if simplify(area - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', area)
