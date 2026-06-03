import numpy as np
a = np.array([4, 1])
b = np.array([-1, -1])
result = a + b
sum_of_components = np.sum(result)
if sum_of_components == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')