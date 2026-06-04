import numpy as np
a = np.array([3, 0])
b = np.array([-1, 2])
result = a + 2*b
component_sum = np.sum(result)
if component_sum == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')