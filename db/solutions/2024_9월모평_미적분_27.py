import numpy as np

def y(x):
    return 0.5 * (abs(np.exp(x) - 1) - np.exp(abs(x)) + 1)

a = -np.log(4)
b = 1.0
N = 2_000_000
xs = np.linspace(a, b, N + 1)
ys = np.array([y(x) for x in xs])
ds = np.sqrt(np.diff(xs)**2 + np.diff(ys)**2)
total = float(ds.sum())

claimed = 23/8
if abs(total - claimed) < 1e-3:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: numeric={total}, claimed={claimed}')
