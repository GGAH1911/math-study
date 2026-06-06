import numpy as np
from scipy.optimize import fsolve

# Given: AB = AC = 1, angle BAC = pi/2
# Triangle ABC: A=(0,0), B=(1,0), C=(0,1)

# Our solution: d = 2/3
d = 2/3
f = 5/12

# Coordinates
A = np.array([0, 0])
B = np.array([1, 0])
C = np.array([0, 1])
D = np.array([1-d, d])
F = np.array([0, f])

# Calculate alpha
alpha = (1-d)**2 + d**2

# Calculate e
e = alpha / (2*(1-d))
E = np.array([e, 0])

# Verify folding condition: A maps to D along perpendicular bisector EF
# Condition 1: EF perpendicular to AD
AD = D - A
EF = F - E
dot_product = np.dot(AD, EF)

# Condition 2: midpoint of AD lies on EF
midpoint_AD = (A + D) / 2
# Check if midpoint is on line EF
# Parametric: P(t) = E + t*EF
# Solve for t
if abs(EF[0]) > 1e-10:
    t = (midpoint_AD[0] - E[0]) / EF[0]
else:
    t = (midpoint_AD[1] - E[1]) / EF[1]

point_on_EF = E + t * EF

# Verify circumradius ratio
# Triangle BDE
BD = np.linalg.norm(D - B)
DE = np.linalg.norm(E - D)
EB = np.linalg.norm(B - E)
area_BDE = abs(np.cross(D - B, E - B)) / 2
R_BDE = (BD * DE * EB) / (4 * area_BDE) if area_BDE > 1e-10 else float('inf')

# Triangle DCF
DC = np.linalg.norm(C - D)
CF = np.linalg.norm(F - C)
FD = np.linalg.norm(D - F)
area_DCF = abs(np.cross(C - D, F - D)) / 2
R_DCF = (DC * CF * FD) / (4 * area_DCF) if area_DCF > 1e-10 else float('inf')

# Verify DF length
DF = np.sqrt((1-d)**2 + (d-f)**2)

# Check all conditions
print("Folding perpendicularity (should be ~0):", dot_product)
print("Midpoint on EF (should be close to [~(1-d)/2, ~d/2]):", point_on_EF)
print("DE:", DE)
print("FD:", FD)
print("DE/FD ratio (should be 2):", DE/FD)
print("Circumradius ratio (should be 2):", R_BDE/R_DCF)
print("DF length:", DF)
print("DF as fraction: 5/12 =", 5/12)
print("\nFinal check:")
if abs(DF - 5/12) < 1e-10:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")