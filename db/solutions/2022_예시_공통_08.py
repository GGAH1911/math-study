import numpy as np

def f(x):
    return 6 * np.sin(np.pi / 12 * x)

# x-coordinates of intersection with y=3
x1, x2 = 2.0, 10.0

y1 = f(x1)
y2 = f(x2)

tol = 1e-9
if abs(y1 - 3) < tol and abs(y2 - 3) < tol:
    length = abs(x2 - x1)
    if abs(length - 8) < tol:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')
