import numpy as np
a, b = 5, 5
alpha, beta = 4, 5
def f(x):
    return (-(x-a)**2 + b) if x <= a else (-np.sqrt(x-a) + b)
assert np.isclose(f(alpha), alpha), f'f(alpha)={f(alpha)} != alpha={alpha}'
assert np.isclose(f(beta), beta), f'f(beta)={f(beta)} != beta={beta}'
result = f(alpha + beta)
assert np.isclose(result, 3), f'f({alpha+beta})={result} != 3'
print('VERIFY_PASS')