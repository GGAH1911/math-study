import numpy as np

def f(x):
    return np.cos(np.pi * x / 6)

def g(x):
    return -3 * np.cos(np.pi * x / 6) - 1

k = 0.5
alpha1, alpha2 = 2, 10
beta1, beta2 = 4, 8

assert abs(f(alpha1) - k) < 1e-10
assert abs(f(alpha2) - k) < 1e-10
assert abs(alpha1 - alpha2) == 8

assert abs(g(beta1) - k) < 1e-10
assert abs(g(beta2) - k) < 1e-10

answer = abs(beta1 - beta2)
if answer == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')