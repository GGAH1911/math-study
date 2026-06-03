from sympy import *

m_val = Rational(2)
a_val = Rational(20, 3)

# Tangent points
Px = 3*a_val/5
Py = 6*a_val/5
Qx = 6*a_val/5
Qy = 3*a_val/5
Ax, Ay = a_val, a_val

# Check P on l1: y = 2x
assert Py == m_val * Px, 'P not on l1'

# Check Q on l2: y = x/2
assert Qy == Qx / m_val, 'Q not on l2'

# Check radius equality (PA = QA)
r = a_val*(m_val - 1)/sqrt(m_val**2 + 1)
PA = sqrt((Ax-Px)**2 + (Ay-Py)**2)
QA = sqrt((Ax-Qx)**2 + (Ay-Qy)**2)
assert simplify(PA - r) == 0, 'PA != r'
assert simplify(QA - r) == 0, 'QA != r'

# R: intersection of PQ with x-axis. PQ slope = -1
Rx = Px + Py  # from y=-x+(Px+Py), set y=0
Ry = Rational(0)

# Condition (가): PQ = QR
PQ = sqrt((Qx-Px)**2 + (Qy-Py)**2)
QR = sqrt((Rx-Qx)**2 + (Ry-Qy)**2)
assert simplify(PQ - QR) == 0, f'PQ={PQ} != QR={QR}'

# Condition (나): area of OPQ = 24
area = Rational(1,2) * abs(Px*Qy - Qx*Py)
assert area == 24, f'area={area}'

# B = intersection of l1 and line AQ
t = symbols('t')
Bx_expr = Ax + t*(Qx - Ax)
By_expr = Ay + t*(Qy - Ay)
t_val = solve(By_expr - m_val*Bx_expr, t)[0]
Bx_val = Ax + t_val*(Qx - Ax)
By_val = Ay + t_val*(Qy - Ay)

# Check B on l1
assert simplify(By_val - m_val*Bx_val) == 0, 'B not on l1'

# BQ
BQ = simplify(sqrt((Bx_val - Qx)**2 + (By_val - Qy)**2))

if BQ == 3*sqrt(5):
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: BQ = {BQ}')
