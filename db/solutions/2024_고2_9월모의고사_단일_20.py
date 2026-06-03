import math

k = math.log2(24)
u = 3
v = math.log2(3)

x_A = k + u
x_B = v - 1

y_A_direct = -x_A + 2*k
y_A_curve = math.log2(x_A - k)

y_B_direct = -x_B + 2*k
y_B_curve = 2**(x_B + 1) + k + 1

dist = math.sqrt((x_A - x_B)**2 + (y_A_direct - y_B_direct)**2)
expected = 7 * math.sqrt(2)

tol = 1e-9
if (abs(y_A_direct - y_A_curve) < tol and 
    abs(y_B_direct - y_B_curve) < tol and 
    abs(dist - expected) < tol):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')