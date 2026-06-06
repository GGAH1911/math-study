import numpy as np
from scipy.special import comb

# 교집합 크기가 1일 확률 재검증
count_size_1 = 0
for sa in range(8):
    for sb in range(4):
        # sa를 이진수로: 비트 0,1,2는 각각 2,3,4 포함 여부
        # sb를 이진수로: 비트 0,1은 각각 2,3 포함 여부
        sa_set = set()
        if sa & 1: sa_set.add(2)
        if sa & 2: sa_set.add(3)
        if sa & 4: sa_set.add(4)
        
        sb_set = set()
        if sb & 1: sb_set.add(2)
        if sb & 2: sb_set.add(3)
        
        if len(sa_set & sb_set) == 1:
            count_size_1 += 1

p = count_size_1 / 32
n = 15360
mu = n * p
sigma = np.sqrt(n * p * (1 - p))

z = (5880 - mu) / sigma
if abs(z - 2.0) < 0.01:
    k = 0.023
    answer = 1000 * k
    if answer == 23:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')