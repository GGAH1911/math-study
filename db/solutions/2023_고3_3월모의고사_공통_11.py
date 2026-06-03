import numpy as np

AB = 2*np.sqrt(2)
BC = 2*np.sqrt(3)
angle_BAC = np.radians(60)
angle_PBC = np.radians(30)
angle_PCB = np.radians(15)

# AC via quadratic AC^2 - 2√2·AC - 4 = 0
AC = (2*np.sqrt(2) + np.sqrt(8 + 16)) / 2  # √2+√6

# Angles
sin_ACB = AB * np.sin(angle_BAC) / BC
angle_ACB = np.arcsin(sin_ACB)
angle_ABC = np.pi - angle_BAC - angle_ACB

# Coordinates: B=(0,0), C=(BC,0)
B = np.array([0.0, 0.0])
C = np.array([float(BC), 0.0])
A = B + AB * np.array([np.cos(angle_ABC), np.sin(angle_ABC)])

# Verify original conditions
assert abs(np.linalg.norm(A-B) - AB) < 1e-9
assert abs(np.linalg.norm(B-C) - BC) < 1e-9
vAB = B - A; vAC = C - A
cos_BAC_calc = np.dot(vAB, vAC) / (np.linalg.norm(vAB)*np.linalg.norm(vAC))
assert abs(cos_BAC_calc - 0.5) < 1e-9

# P via law of sines in △BPC
angle_BPC = np.pi - angle_PBC - angle_PCB
BP = BC * np.sin(angle_PCB) / np.sin(angle_BPC)
CP = BC * np.sin(angle_PBC) / np.sin(angle_BPC)
P = B + BP * np.array([np.cos(angle_PBC), np.sin(angle_PBC)])

# Verify ∠PBC=30°
vBP = P - B; vBC = C - B
ang1 = np.degrees(np.arccos(np.dot(vBP,vBC)/(np.linalg.norm(vBP)*np.linalg.norm(vBC))))
assert abs(ang1 - 30) < 1e-6

# Verify ∠PCB=15°
vCP = P - C; vCB = B - C
ang2 = np.degrees(np.arccos(np.dot(vCP,vCB)/(np.linalg.norm(vCP)*np.linalg.norm(vCB))))
assert abs(ang2 - 15) < 1e-6

# Area of △APC
v1 = P - A; v2 = C - A
area_APC = 0.5 * abs(v1[0]*v2[1] - v1[1]*v2[0])
expected = (3 + np.sqrt(3)) / 2

if abs(area_APC - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: computed={area_APC:.10f}, expected={expected:.10f}')