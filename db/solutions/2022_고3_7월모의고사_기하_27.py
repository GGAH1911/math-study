import numpy as np

# Points
A = np.array([0.0, 0.0, 0.0])
B = np.array([4*np.sqrt(5), 0.0, 0.0])
C = np.array([4*np.sqrt(5), 6.0, 0.0])
D = np.array([2*np.sqrt(5), 0.0, 4.0])

# Verify original conditions
AC = np.linalg.norm(C - A)
BC = np.linalg.norm(C - B)
AD = np.linalg.norm(D - A)
BD = np.linalg.norm(D - B)

eps = 1e-9
ok = True
if abs(AC - 2*np.sqrt(29)) > eps: print(f'FAIL AC={AC}'); ok=False
if abs(BC - 6) > eps: print(f'FAIL BC={BC}'); ok=False
if abs(AD - 6) > eps: print(f'FAIL AD={AD}'); ok=False
if abs(BD - 6) > eps: print(f'FAIL BD={BD}'); ok=False

# angle ABC = pi/2
BA = A - B
BC_vec = C - B
if abs(np.dot(BA, BC_vec)) > eps: print('FAIL angle ABC'); ok=False

# D on plane beta (xOz, y=0)
if abs(D[1]) > eps: print('FAIL D not on beta'); ok=False

# C on plane alpha (xOy, z=0)
if abs(C[2]) > eps: print('FAIL C not on alpha'); ok=False

# Compute cos theta
CD_dir = D - C
n = np.array([0.0, 0.0, 1.0])
sin_theta = abs(np.dot(CD_dir, n)) / np.linalg.norm(CD_dir)
cos_theta = np.sqrt(max(0, 1 - sin_theta**2))
expected = np.sqrt(7)/3

if ok and abs(cos_theta - expected) < eps:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL cos_theta={cos_theta:.10f} expected={expected:.10f}')
