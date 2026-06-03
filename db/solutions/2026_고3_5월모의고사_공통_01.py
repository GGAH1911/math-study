import numpy as np
result = 2**(1/3) * 32**(1/3)
answer = 4
if abs(result - answer) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')