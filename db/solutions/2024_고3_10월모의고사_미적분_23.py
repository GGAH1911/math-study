import numpy as np

# 원래 함수: (e^{3x} - 1) / ln(1 + 2x)
# x -> 0 극한을 수치적으로 확인
results = []
for x in [1e-4, 1e-6, 1e-8, 1e-10]:
    val = (np.exp(3*x) - 1) / np.log(1 + 2*x)
    results.append(val)

limit_approx = results[-1]
expected = 3/2

if abs(limit_approx - expected) < 1e-6:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {limit_approx}, expected {expected}')
