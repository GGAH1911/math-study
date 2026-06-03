import numpy as np

A = np.array([-3.0, 2.0])
B = np.array([5.0, 4.0])
A_prime = np.array([-3.0, -2.0])  # A reflected across x-axis

# Numerical minimization over Q on x-axis and P on circle centered at B, radius 3
min_val = float('inf')
best_q = None
best_p = None
for angle in np.linspace(0, 2*np.pi, 5000):
    P = B + 3.0 * np.array([np.cos(angle), np.sin(angle)])
    # For fixed P, optimal Q is on segment A'P intersecting x-axis
    # Parametric: A' + t*(P - A'), y=0 => t = -A'[1]/(P[1]-A'[1])
    if abs(P[1] - A_prime[1]) < 1e-12:
        # same y, check direct
        for qx in np.linspace(-20, 20, 2000):
            Q = np.array([qx, 0.0])
            val = np.linalg.norm(A - Q) + np.linalg.norm(Q - P)
            if val < min_val:
                min_val = val
                best_q, best_p = Q.copy(), P.copy()
    else:
        t = -A_prime[1] / (P[1] - A_prime[1])
        if 0 <= t <= 1:
            Q = A_prime + t * (P - A_prime)
            val = np.linalg.norm(A - Q) + np.linalg.norm(Q - P)
        else:
            # Q outside segment, check boundary t=0 and t=1 and direct search
            val = np.linalg.norm(A - A_prime) + np.linalg.norm(A_prime - P)  # won't be min
        if val < min_val:
            min_val = val
            best_q = A_prime + t*(P - A_prime) if 0<=t<=1 else None
            best_p = P.copy()

# Theoretical
A_prime_B = np.linalg.norm(A_prime - B)
theoretical = A_prime_B - 3.0

if abs(min_val - 7.0) < 0.05 and abs(theoretical - 7.0) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: numerical={min_val:.4f}, theoretical={theoretical:.4f}')
