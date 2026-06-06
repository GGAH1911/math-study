import numpy as np
from scipy.optimize import fsolve

def verify():
    count = 0
    for p in range(1, 26):
        for q in range(1, 26):
            # 조건 (가): q < 4p^3
            if not (q < 4*p**3):
                continue
            
            # 조건 (나): [-1,1]과 [-2,2]에서 |f(x)| 최댓값이 같음
            def f(x):
                return x**3 - 3*p*x**2 + q
            
            max1 = max(abs(f(x)) for x in [-1, 0, 1])
            max2 = max(abs(f(x)) for x in [-2, -1, 0, 1, 2])
            
            if max1 == max2:
                count += 1
    
    return count

result = verify()
if result == 14:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')