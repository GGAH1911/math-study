from itertools import combinations

U = {1, 3, 5, 7, 9}
U_sum = sum(U)
valid_sums = []

for A_size in range(2, 6):
    for A in combinations(U, A_size):
        A = set(A)
        A_complement = U - A
        
        for AB in combinations(A, 2):
            AB = set(AB)
            B = A_complement | AB
            
            if len(A & B) == 2:
                AUB_minus_AIB = (A | B) - (A & B)
                s = sum(AUB_minus_AIB)
                valid_sums.append(s)

if valid_sums:
    M = max(valid_sums)
    m = min(valid_sums)
    result = M + m
    if result == 30:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')