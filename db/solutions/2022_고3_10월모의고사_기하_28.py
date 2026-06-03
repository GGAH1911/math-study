import numpy as np
sqrt3 = np.sqrt(3)
C = np.array([6.0, 2*sqrt3])
thetas = np.linspace(0, 2*np.pi/3, 200000)
max_val = -np.inf
min_val = np.inf
for theta in thetas:
    P = np.array([4*np.cos(theta), 4*np.sin(theta)])
    dot_OC = np.dot(P, C)
    fmax = dot_OC + 4 - 16
    fmin = dot_OC - 4 - 16
    if fmax > max_val: max_val = fmax
    if fmin < min_val: min_val = fmin
result = max_val + min_val
expected = 16*sqrt3 - 32
print(f'M={max_val:.6f}, m={min_val:.6f}, M+m={result:.6f}, expected={expected:.6f}')
if abs(result - expected) < 0.005:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')