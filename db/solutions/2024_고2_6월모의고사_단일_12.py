import numpy as np
k = 5
xs = np.linspace(-2*np.pi, 2*np.pi, 200001)
f = 2*np.cos(xs)**2 + 2*np.sin(xs) + k
fmax = f.max(); fmin = f.min()
print('VERIFY_PASS' if abs(fmax - 15/2) < 1e-6 and abs(fmin - 3) < 1e-6 else 'VERIFY_FAIL')