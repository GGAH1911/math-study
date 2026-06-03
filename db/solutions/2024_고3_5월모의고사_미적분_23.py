import math

def f_double_prime(x):
    return -4 * math.sin(2 * x)

result = f_double_prime(math.pi / 4)
expected = -4

if abs(result - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {result}')