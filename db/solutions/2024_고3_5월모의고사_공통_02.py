import numpy as np

# 원래 함수: sqrt(x^2 + 4x) - x
def f(x):
    return np.sqrt(x**2 + 4*x) - x

# x가 충분히 큰 값들에서 함수값 계산
test_values = [1e3, 1e4, 1e5, 1e6, 1e7]
results = [f(x) for x in test_values]

# 모든 값이 2에 수렴하는지 확인
expected = 2
all_close = all(abs(r - expected) < 1e-2 for r in results)

if all_close:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')