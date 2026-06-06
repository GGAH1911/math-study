import numpy as np
from scipy.optimize import minimize_scalar

# Coordinates
A = np.array([0.0, 0.0])
B = np.array([6.0, 0.0])
D = np.array([-1.0, np.sqrt(15)])
C = np.array([5.0, np.sqrt(15)])

# Center of constraint circle
G = (A + B + C + D) / 4

# Find maximum of |PB|^2 where P is on circle centered at G with radius 1
max_val = 0
for theta in np.linspace(0, 2*np.pi, 10000):
    P = G + np.array([np.cos(theta), np.sin(theta)])
    Q = C - P
    
    PB = B - P
    DQ = Q - D
    
    dot_product = np.dot(PB, DQ)
    max_val = max(max_val, dot_product)

# Verify the answer is 25
if abs(max_val - 25) < 0.01:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {max_val}, expected 25')