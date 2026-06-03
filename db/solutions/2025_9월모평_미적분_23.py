import numpy as np

# lim_{x->0} sin(5x)/x 수치 검증
x_vals = [1e-5, 1e-6, 1e-7, 1e-8, 1e-9]
results = [np.sin(5*x)/x for x in x_vals]
expected = 5

if all(abs(v - expected) < 1e-5 for v in results):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(results)
