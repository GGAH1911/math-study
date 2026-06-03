import numpy as np
k = 3
A = np.array([[1, 3], [k, 5]])
B = np.array([[k, 1], [-2, 4]])
AB = A @ B
if AB[0,1] == 13 and AB[1,0] == -1:
    a, b = AB[0,0], AB[1,1]
    if a + b == 20:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')