from sympy import *
p = Rational(5, 8)
y0 = 2*sqrt(6)
x0 = y0**2 / (4*p)
y1 = 3*sqrt(6)
x1 = y1**2 / (4*p)
P = (x0, y0)
Q = (x1, y1)
F = (p, Integer(0))
# P on C1
assert simplify(y0**2 - 4*p*x0) == 0, 'P not on C1'
# Q on C1
assert simplify(y1**2 - 4*p*x1) == 0, 'Q not on C1'
# Q on C2: (x-x0)^2 = 4*y0*y
assert simplify((x1-x0)**2 - 4*y0*y1) == 0, 'Q not on C2'
# H = foot from Q to directrix y=-y0
H = (x1, -y0)
# PH = 4*sqrt(15)
PH = sqrt((P[0]-H[0])**2 + (P[1]-H[1])**2)
assert simplify(PH - 4*sqrt(15)) == 0, f'PH={PH}'
# QH = 5*sqrt(6)
QH = sqrt((Q[0]-H[0])**2 + (Q[1]-H[1])**2)
assert simplify(QH - 5*sqrt(6)) == 0, f'QH={QH}'
# x_P > x_F
assert x0 > p, 'x_P <= x_F'
# PF via focal-directrix
PF = x0 + p
assert PF == Rational(409,40), f'PF={PF}'
print('VERIFY_PASS')