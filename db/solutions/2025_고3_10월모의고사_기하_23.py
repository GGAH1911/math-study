import numpy as np
a = np.array([-1, 2])
b = np.array([1, 1])
result = a + 2*b
component_sum = sum(result)
if component_sum == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')