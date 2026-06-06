import math
a = -4
b = 2/3
def f(x):
    return a * math.cos(b * x) + 10 - a
result = f(math.pi / 2)
expected = 12
if abs(result - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')