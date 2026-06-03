import numpy as np

sqrt2 = np.sqrt(2)
sqrt5 = np.sqrt(5)
sqrt10 = np.sqrt(10)

# Coordinates from solution
B = np.array([0.0, 0.0])
C = np.array([10*sqrt2, 0.0])
A = np.array([2*sqrt2, 4*sqrt2])
D = np.array([12*sqrt2, 4*sqrt2])

# Check parallelogram: AB = DC
ok = True
if not np.allclose(A - B, D - C): ok = False

# E = foot of perpendicular from A to BD
BD = D - B
t = np.dot(A - B, BD) / np.dot(BD, BD)
E = B + t * BD

# AE perp BD
if not np.isclose(np.dot(E - A, BD), 0, atol=1e-9): ok = False

# F = intersection of line CE with AB, parameter lambda = t/(1-t)
lam = t / (1 - t)
F = lam * A  # on line from B through A

# F on line CE?
CE_dir = E - C
CF = F - C
cross = CF[0]*CE_dir[1] - CF[1]*CE_dir[0]
if not np.isclose(cross, 0, atol=1e-9): ok = False

# lambda in [0,1]
if not (0 <= lam <= 1): ok = False

# Condition 1: cos(angle AFC) = sqrt(10)/10
FA = A - F
FC = C - F
cos_AFC = np.dot(FA, FC) / (np.linalg.norm(FA) * np.linalg.norm(FC))
if not np.isclose(cos_AFC, sqrt10/10, atol=1e-9): ok = False

# Condition 2: EC = 10
if not np.isclose(np.linalg.norm(C - E), 10.0, atol=1e-9): ok = False

# Condition 3: circumradius of CDE = 5*sqrt(2)
a = np.linalg.norm(D - E)  # side opposite C
b = np.linalg.norm(C - E)  # side opposite D
c = np.linalg.norm(D - C)  # side opposite E
area_CDE = 0.5 * abs((D[0]-C[0])*(E[1]-C[1]) - (E[0]-C[0])*(D[1]-C[1]))
R = a * b * c / (4 * area_CDE)
if not np.isclose(R, 5*sqrt2, atol=1e-9): ok = False

# Area of triangle AFE (the answer)
AF = F - A
AE = E - A
area_AFE = 0.5 * abs(AF[0]*AE[1] - AF[1]*AE[0])
if not np.isclose(area_AFE, 20/3, atol=1e-9): ok = False

print('VERIFY_PASS' if ok else f'VERIFY_FAIL: area={area_AFE:.6f}, R={R:.6f}, EC={np.linalg.norm(C-E):.6f}, cos_AFC={cos_AFC:.6f}')
