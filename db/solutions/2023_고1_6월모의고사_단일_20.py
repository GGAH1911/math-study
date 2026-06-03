import numpy as np

def f(x, a):
    return (x - a)**2

# Find all a in [2,10] satisfying both conditions
valid_a = []
for a in np.linspace(2, 10, 100001):
    xs1 = np.linspace(2, 10, 2001)
    if abs(np.min(f(xs1, a))) > 1e-9:
        continue
    xs2 = np.linspace(2, 6, 2001)
    xs3 = np.linspace(6, 10, 2001)
    max26 = np.max(f(xs2, a))
    min610 = np.min(f(xs3, a))
    if abs(max26 - min610) < 1e-6:
        valid_a.append(a)

vals = [f(-1, a) for a in valid_a]
M = max(vals)
m = min(vals)
result = M + m
if abs(result - 34) < 1e-3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', M, m, result)
