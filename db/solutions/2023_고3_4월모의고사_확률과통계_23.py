from math import comb

# 중복순열: nPi_r = n^r
nPi = 3**2  # _3Pi_2

# 중복조합: nH_r = C(n+r-1, r)
nH = comb(2+3-1, 3)  # _2H_3

result = nPi + nH

if result == 13:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
