import math

a = 1
b = 3

def f(x):
    return math.log(x - a, 0.5) + b

max_val = f(2)  # decreasing function, max at left endpoint
min_val = f(5)  # decreasing function, min at right endpoint

if abs(max_val - 3) < 1e-9 and abs(min_val - 1) < 1e-9 and a + b == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
