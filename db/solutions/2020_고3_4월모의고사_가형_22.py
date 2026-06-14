CANDIDATE = 43
from math import comb, factorial

# 중복순열: nPi_r = n^r
n1, r1 = 6, 2
npi = n1 ** r1  # = 36

# 중복조합: nH_r = C(n+r-1, r)
n2, r2 = 2, 6
nh = comb(n2 + r2 - 1, r2)  # = C(7,6) = 7

result = npi + nh

if CANDIDATE == result:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: expected {result}, got {CANDIDATE}')
