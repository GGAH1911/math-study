import numpy as np

n = 14
valid_count = 0

for x in range(-30, 30):
    # 밑의 조건
    if x == -1 or x == 0 or x == -2:
        continue
    
    # 진수 조건: (n-x)(n+1+x) > 0
    arg = (n - x) * (n + 1 + x)
    if arg > 0:
        valid_count += 1

if valid_count == 25:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')