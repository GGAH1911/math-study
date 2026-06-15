from itertools import combinations

CANDIDATE = 6

# 집합 정의
A = {1, 2, 4, 8, 16}
B = {x for x in range(1, 20) if x**2 - 4*x + 3 == 0}
A_minus_B = A - B

# 조건을 만족하는 X의 개수 계산
count = 0
for X in combinations(A_minus_B, 2):
    X_set = set(X)
    # 조건 1: n(X) = 2
    if len(X_set) != 2:
        continue
    # 조건 2: X - (A-B) = ∅ ⟺ X ⊆ (A-B)
    if not (X_set <= A_minus_B):
        continue
    count += 1

if count == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')