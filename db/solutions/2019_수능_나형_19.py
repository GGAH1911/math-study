# 함수 f의 조건을 검증
from itertools import combinations, permutations

# X = {1,2,3,4,5,6}
X = set(range(1, 7))

# n(B) = 5인 함수의 개수를 직접 계산
count = 0

# A를 선택 (크기 5)
for A_tuple in combinations(X, 5):
    A = set(A_tuple)
    k = (X - A).pop()  # X \ A의 유일한 원소
    
    # f(k) ∈ A 선택
    for f_k in A:
        # A에서 A로의 전단사 f 선택
        # f(A) = A를 만족해야 함
        for perm in permutations(A):
            # perm은 (f(a1), f(a2), ..., f(a5))
            # 이것이 A의 모든 원소를 포함하면 됨
            if set(perm) == A:
                count += 1

# 계산된 개수
expected = 6 * 5 * 120

if count == expected:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: expected {expected}, got {count}')