import numpy as np
from sympy import *

a2, b2, c2 = 24, 8, 16
a_val = sqrt(a2)
b_val = sqrt(b2)
c_val = sqrt(c2)

# Points
xP = Rational(9,2); yP = sqrt(5)/2
xQ = Integer(3); yQ = -sqrt(5)

# Check P on ellipse
assert simplify(xP**2/a2 + yP**2/b2 - 1) == 0, 'P not on ellipse'
# Check Q on ellipse
assert simplify(xQ**2/a2 + yQ**2/b2 - 1) == 0, 'Q not on ellipse'

# F = (c, 0) = (4, 0)
F = Matrix([c_val, 0])
Fp = Matrix([-c_val, 0])
P = Matrix([xP, yP])
Q = Matrix([xQ, yQ])

PF = (P - F).norm()
QF = (Q - F).norm()
FF_prime = (F - Fp).norm()

# Check PF/QF = 1/2
assert simplify(PF/QF - Rational(1,2)) == 0, f'PF/QF failed: {PF/QF}'
# Check PF/FF' = sqrt(6)/16
assert simplify(PF/FF_prime - sqrt(6)/16) == 0, f'PF/FF failed: {PF/FF_prime}'

# Area of triangle FF'Q
base = FF_prime
height = Abs(yQ)
area = Rational(1,2) * base * height
assert simplify(area - 4*sqrt(5)) == 0, f'Area failed: {area}'

print('VERIFY_PASS')
