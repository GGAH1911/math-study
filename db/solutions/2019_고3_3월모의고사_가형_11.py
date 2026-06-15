import math
a = -math.pi
x = 0.5
u = math.pi * x**2 + a * x
k = math.tan(u)
expected = -1
if math.isclose(k, expected, abs_tol=1e-9):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')