import numpy as np
a = np.array([2, 6])
b = np.array([2, -6])
sum_vec = a + b
component_sum = np.sum(sum_vec)
result = 'VERIFY_PASS' if component_sum == 4 else 'VERIFY_FAIL'
print(result)