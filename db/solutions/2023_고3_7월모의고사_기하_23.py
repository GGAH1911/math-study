import numpy as np
a = np.array([2, 3])
b = np.array([4, -2])
result = 2*a + b
sum_components = np.sum(result)
if sum_components == 12:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')