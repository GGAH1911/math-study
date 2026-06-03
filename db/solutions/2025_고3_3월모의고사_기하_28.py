import numpy as np

# Given: C1: y^2=12x (F1=(3,0)), C2: y^2=-6x (F2=(-3/2,0))
a = 8
P = (a**2/12, a)
Q = (-a**2/6, a)
F1 = (3.0, 0.0)
F2 = (-1.5, 0.0)

# Verify P on C1, Q on C2
assert abs(P[1]**2 - 12*P[0]) < 1e-9, 'P not on C1'
assert abs(Q[1]**2 - (-6)*Q[0]) < 1e-9, 'Q not on C2'

# Perimeter
PQ = abs(P[0] - Q[0])
QF2 = np.sqrt((Q[0]-F2[0])**2 + (Q[1]-F2[1])**2)
F2F1 = np.sqrt((F2[0]-F1[0])**2 + (F2[1]-F1[1])**2)
F1P = np.sqrt((F1[0]-P[0])**2 + (F1[1]-P[1])**2)
perimeter = PQ + QF2 + F2F1 + F1P

# Area via Shoelace
verts = [P, Q, F2, F1]
n = len(verts)
area = 0
for i in range(n):
    j = (i+1) % n
    area += verts[i][0]*verts[j][1] - verts[j][0]*verts[i][1]
area = abs(area) / 2

if abs(perimeter - 41) < 1e-6 and abs(area - 82) < 1e-6:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: perimeter={perimeter}, area={area}')
