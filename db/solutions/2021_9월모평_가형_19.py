from itertools import combinations

# X의 공집합이 아닌 모든 부분집합 생성
X = {1, 2, 3, 4}
subsets = []
for i in range(1, 5):
    for combo in combinations(X, i):
        subsets.append(frozenset(combo))

# A ⊂ B ⊂ C를 만족하는 순서쌍 (A, B, C) 개수 세기
count_valid = 0
total_count = 0

for A in subsets:
    for B in subsets:
        if A == B:  # A와 B가 다른 경우만
            continue
        for C in subsets:
            if C == A or C == B:  # C는 A, B와 달라야 함
                continue
            total_count += 1
            # A ⊂ B ⊂ C 확인
            if A.issubset(B) and B.issubset(C):
                count_valid += 1

total = 15 * 14 * 13
if count_valid == 60 and total == 2730:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')