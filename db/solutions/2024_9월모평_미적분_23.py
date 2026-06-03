import numpy as np

def f(x):
    if abs(x) < 1e-15:
        return None
    return (np.exp(7*x) - 1) / (np.exp(2*x) - 1)

# 수치적으로 x->0 극한 확인
xs = [1e-3, 1e-5, 1e-7, 1e-9]
vals = [f(x) for x in xs]
limit_numerical = vals[-1]
expected = 7/2

if abs(limit_numerical - expected) < 1e-6:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: numerical={limit_numerical}, expected={expected}')
