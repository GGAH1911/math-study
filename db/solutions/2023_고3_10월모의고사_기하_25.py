import numpy as np

# Setup coordinates: AB along x-axis, plane alpha = z=0
# A=(-3,0,0), B=(3,0,0), C=(cx,4,0) where 4 = height from C to AB
# P=(cx,4,2) since PC=2 perpendicular to plane alpha

cx = 0.0  # x-position of C doesn't affect the distance
A = np.array([-3.0, 0.0, 0.0])
B = np.array([3.0, 0.0, 0.0])
C = np.array([cx, 4.0, 0.0])
P = np.array([cx, 4.0, 2.0])

# Verify conditions
AB_len = np.linalg.norm(B - A)
AC = C - A
BC = C - B
area = 0.5 * np.linalg.norm(np.cross(B - A, C - A))
PC_len = np.linalg.norm(P - C)

# Check PC perpendicular to plane alpha (z-component only)
PC_vec = P - C
perp_ok = abs(PC_vec[0]) < 1e-9 and abs(PC_vec[1]) < 1e-9

# Distance from P to line AB
direction = (B - A) / np.linalg.norm(B - A)
AP = P - A
cross = np.cross(AP, direction)
dist_P_AB = np.linalg.norm(cross)

expected = 2 * np.sqrt(5)

if (abs(AB_len - 6) < 1e-9 and abs(area - 12) < 1e-9 and
    abs(PC_len - 2) < 1e-9 and perp_ok and
    abs(dist_P_AB - expected) < 1e-9):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'AB={AB_len}, area={area}, PC={PC_len}, perp={perp_ok}, dist={dist_P_AB}, expected={expected}')
