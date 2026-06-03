from math import factorial
from itertools import product as iproduct

# Brute force verification
# 5 days, each day assigned one pair from {AC, AD, BC, BD, CD} (AB excluded)
pairs = ['AC','AD','BC','BD','CD']

count = 0
for days in iproduct(range(5), repeat=5):
    # days[i] = index of pair assigned to day i
    n = [days.count(i) for i in range(5)]
    # n[0]=n_AC, n[1]=n_AD, n[2]=n_BC, n[3]=n_BD, n[4]=n_CD
    n_AC, n_AD, n_BC, n_BD, n_CD = n
    
    # (나) n_AB = 0 (already excluded)
    # (다) n_BC = 1
    if n_BC != 1:
        continue
    # (가) each sport >= 2 days
    A_days = n_AC + n_AD          # A appears in AC, AD
    B_days = n_BC + n_BD          # B appears in BC, BD
    C_days = n_AC + n_BC + n_CD   # C appears in AC, BC, CD
    D_days = n_AD + n_BD + n_CD   # D appears in AD, BD, CD
    if A_days < 2 or B_days < 2 or C_days < 2 or D_days < 2:
        continue
    count += 1

if count == 450:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {count}')
