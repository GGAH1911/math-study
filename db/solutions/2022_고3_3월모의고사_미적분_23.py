import numpy as np

def check_limit():
    results = []
    for n in range(100, 200):
        num = 2**(n+1) + 3**(n-1)
        den = (-2)**n + 3**n
        results.append(num / den)
    limit = results[-1]
    target = 1/3
    if abs(limit - target) < 1e-9:
        print('VERIFY_PASS')
    else:
        print(f'VERIFY_FAIL: got {limit}, expected {target}')

check_limit()
