import math
a = 4
b = -2
x_test = 5
y_test = 0
y_computed = math.log(x_test + a, 3) + b
if abs(y_computed - y_test) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')