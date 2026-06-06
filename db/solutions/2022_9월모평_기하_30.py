import numpy as np
from scipy.optimize import fsolve

# 기본 점들
A = np.array([-3, 1])
B = np.array([0, 2])
C = np.array([1, 0])
O = np.array([0, 0])

# P0, Q0
theta0 = -np.pi/4
phi0 = 3*np.pi/4
P0 = A + np.array([np.cos(theta0), np.sin(theta0)])
Q0 = B + 2*np.array([np.cos(phi0), np.sin(phi0)])

# X at boundary condition
t_boundary = np.sqrt(2) - 0.5
X = A + t_boundary * np.array([np.cos(theta0), np.sin(theta0)])

# Check condition
condition_value = np.dot(X - B, Q0 - B)
print(f"Condition: {condition_value:.10f} (should be 1.0)")

# Calculate |Q0X|^2
Q0X = X - Q0
dist_sq = np.dot(Q0X, Q0X)
expected = 41/4
print(f"|Q0X|^2 = {dist_sq:.10f}")
print(f"Expected: {expected:.10f}")

if abs(dist_sq - expected) < 1e-10:
    print("VERIFY_PASS")
else:
    print(f"VERIFY_FAIL")
    print(f"Difference: {abs(dist_sq - expected)}")