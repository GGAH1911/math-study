from math import comb

# A(0,0) → P(2,1) → B(4,3)
# A에서 P까지: 우 2, 상 1
path_AP = comb(3, 2)  # C(3,2) = 3

# P에서 B까지: 우 2, 상 2  
path_PB = comb(4, 2)  # C(4,2) = 6

total = path_AP * path_PB
print('VERIFY_PASS' if total == 18 else 'VERIFY_FAIL')