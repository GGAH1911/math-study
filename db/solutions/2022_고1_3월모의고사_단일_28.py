import numpy as np
data = [3, 4, 4, 5, 9, 9, 10, 12]
mean = np.mean(data)
median = (np.sort(data)[3] + np.sort(data)[4]) / 2
variance = np.var(data)
if abs(mean - 7) < 1e-9 and abs(median - 7) < 1e-9 and abs(variance - 10) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')