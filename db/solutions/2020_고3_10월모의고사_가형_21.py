import numpy as np
from scipy.optimize import fsolve

def compute_area(theta):
    # Points
    A = np.array([0.0, 0.0])
    B = np.array([2.0, 0.0])
    P = np.array([1 + np.cos(2*theta), np.sin(2*theta)])
    
    # C position using sine rule
    c = 2*np.cos(theta)*np.sin(2*theta) / np.sin(3*theta)
    C = np.array([c, 0.0])
    
    # Line CD perpendicular to CP
    CP = P - C
    perp = np.array([-CP[1], CP[0]])  # perpendicular to CP
    perp = perp / np.linalg.norm(perp)
    
    # D on circle with diameter AC and on line through C perpendicular to CP
    center = (A + C) / 2
    radius = np.linalg.norm(C - A) / 2
    
    # Parametric line: C + s*perp
    # (C + s*perp - center)·(C + s*perp - center) = radius²
    v = C - center
    a = np.dot(perp, perp)  # = 1
    b = 2*np.dot(v, perp)
    c_coef = np.dot(v, v) - radius**2
    
    disc = b**2 - 4*a*c_coef
    s1 = (-b + np.sqrt(disc))/(2*a)
    s2 = (-b - np.sqrt(disc))/(2*a)
    
    D1 = C + s1*perp
    D2 = C + s2*perp
    # Choose D away from C
    D = D1 if np.linalg.norm(D1 - C) > np.linalg.norm(D2 - C) else D2
    
    # E: intersection of AP and CD
    # Line AP: A + t*(P-A) = t*P
    # Line CD: C + s*perp
    # t*P[0] = C[0] + s*perp[0]
    # t*P[1] = C[1] + s*perp[1]
    
    # From first: t = (C[0] + s*perp[0])/P[0]
    # Substitute to second: ((C[0] + s*perp[0])/P[0])*P[1] = C[1] + s*perp[1]
    t = (C[0]) / P[0] if abs(P[0]*perp[1] - P[1]*perp[0]) > 1e-10 else 0
    # More careful: solve the 2x2 system
    A_mat = np.array([[P[0], -perp[0]], [P[1], -perp[1]]])
    b_vec = np.array([C[0], C[1]])
    params = np.linalg.solve(A_mat, b_vec)
    t_E, s_E = params
    E = t_E * P
    
    # Area of triangle DEP
    v1 = E - D
    v2 = P - D
    area = 0.5 * abs(v1[0]*v2[1] - v1[1]*v2[0])
    
    return area, P, C, D, E

# Test for small theta
theta_vals = [0.01, 0.005, 0.001]
for theta in theta_vals:
    area, P, C, D, E = compute_area(theta)
    ratio = area / theta
    print(f"theta={theta}: S(θ)={area:.10f}, S(θ)/θ={ratio:.10f}")

print(f"Expected limit: 8/9 = {8/9:.10f}")

# High precision check
theta = 1e-6
area, _, _, _, _ = compute_area(theta)
ratio = area / theta
if abs(ratio - 8/9) < 0.01:
    print("VERIFY_PASS")
else:
    print(f"VERIFY_FAIL: got {ratio}, expected {8/9}")