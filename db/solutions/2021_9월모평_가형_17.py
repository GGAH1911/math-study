from itertools import permutations
from math import gcd

clubs = list(range(7))  # 0: A, 1: B, 2~6: 과학
count_P = 0
count_Q = 0
count_PQ = 0
total = 0

for perm in permutations(clubs):
    total += 1
    pos_A = perm.index(0)
    pos_B = perm.index(1)
    
    if pos_A < pos_B:
        count_P += 1
    
    if abs(pos_A - pos_B) == 3:
        count_Q += 1
        if pos_A < pos_B:
            count_PQ += 1

count_union = count_P + count_Q - count_PQ
if count_union == 3000 and total == 5040:
    g = gcd(count_union, total)
    if count_union // g == 25 and total // g == 42:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')