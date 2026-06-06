import numpy as np
count = 0
for x in range(1, 1000):
    if (1.0/3.0)**(x-7) >= 9:
        count += 1
print('VERIFY_PASS' if count == 5 else 'VERIFY_FAIL')