import numpy as np

def f(x):
    return (4**x - 1) / x

# 수치 극한 확인
xs = [1e-6, 1e-7, 1e-8]
result = np.mean([f(x) for x in xs])
expected = 2 * np.log(2)

if abs(result - expected) < 1e-5:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {result}, expected {expected}')
