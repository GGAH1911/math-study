import numpy as np

answer = 2
result = 4 * np.cos(np.pi / 3)

if abs(result - answer) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')