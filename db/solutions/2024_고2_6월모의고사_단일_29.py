import numpy as np
from scipy.optimize import fsolve

sqrt7 = np.sqrt(7)

# 임의의 d > 0 선택 (AC > 2√7 만족)
d = 4

A = np.array([0.0, 0.0])
D = np.array([float(d), 0.0])
C = np.array([d + 2*sqrt7, 0.0])
B = np.array([d - 3*sqrt7, 9.0])

# Verify conditions:
# 1. CD = 2√7
CD = np.linalg.norm(C - D)
assert abs(CD - 2*sqrt7) < 1e-9, f'CD check failed: {CD} vs {2*sqrt7}'

# 2. cos(∠BDA) = √7/4
DA = A - D
DB = B - D
cos_BDA = np.dot(DA, DB) / (np.linalg.norm(DA) * np.linalg.norm(DB))
assert abs(cos_BDA - sqrt7/4) < 1e-9, f'cos(∠BDA) check failed: {cos_BDA} vs {sqrt7/4}'

# 3. BC + BD = 28
BC = np.linalg.norm(C - B)
BD = np.linalg.norm(D - B)
result = BC + BD
assert abs(result - 28) < 1e-9, f'BC + BD check failed: {result}'

# 4. Verify R₁:R₂ = 4:3
AB = np.linalg.norm(B - A)
AC = np.linalg.norm(C - A)
AD = np.linalg.norm(D - A)

S1 = 0.5 * abs(A[0]*(B[1]-C[1]) + B[0]*(C[1]-A[1]) + C[0]*(A[1]-B[1]))
S2 = 0.5 * abs(A[0]*(B[1]-D[1]) + B[0]*(D[1]-A[1]) + D[0]*(A[1]-B[1]))

R1 = (AB * BC * AC) / (4 * S1)
R2 = (AB * BD * AD) / (4 * S2)
ratio = R1 / R2

assert abs(ratio - 4/3) < 1e-9, f'R₁:R₂ check failed: {ratio} vs {4/3}'

print('VERIFY_PASS')