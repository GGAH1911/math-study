import numpy as np

def f(x):
    return 2**x + 2*x**2 - 2

def bisect_method(f, a, b, tol=1e-11):
    while b - a > tol:
        mid = (a + b) / 2
        if f(a) * f(mid) < 0:
            b = mid
        else:
            a = mid
    return (a + b) / 2

x1 = bisect_method(f, -1.0, 0.0)
x2 = bisect_method(f, 0.0, 1.0)

y1 = 2**x1
y2 = 2**x2

check_a = x2 > 0.5
check_b = y2 - y1 < x2 - x1
y1y2 = y1 * y2
sqrt2_half = np.sqrt(2) / 2
check_c = sqrt2_half < y1y2 < 1.0

if check_a and check_b and check_c:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')