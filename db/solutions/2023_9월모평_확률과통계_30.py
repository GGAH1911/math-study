from itertools import combinations, permutations

X = {1, 2, 3, 4, 5}
count = 0

# n(A) = 2
for A_tuple in combinations(X, 2):
    A = set(A_tuple)
    X_minus_A = X - A
    # f|_A는 고정된 교환: 나머지는 A로 자유롭게
    count += 2 ** len(X_minus_A)  # 2^3 = 8

# n(A) = 3
for A_tuple in combinations(X, 3):
    A = set(A_tuple)
    X_minus_A = X - A
    A_list = sorted(A)
    
    # A의 derangement 찾기
    derangements = 0
    for perm in permutations(A_list):
        if all(perm[i] != A_list[i] for i in range(3)):
            derangements += 1
    
    count += derangements * (3 ** len(X_minus_A))  # 2 * 3^2

if count == 260:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {count}')