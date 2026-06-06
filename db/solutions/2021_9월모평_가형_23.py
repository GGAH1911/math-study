import math

def f_prime(x):
    return math.log(2*x - 1) + (2*x) / (2*x - 1)

result = f_prime(1)
expected = 2

if abs(result - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')