# 주어진 집합
A = {1, 2, 3, 4}
B = {3, 4, 5, 6}
A_union_B = A.union(B)  # {1, 2, 3, 4, 5, 6}

# 가능한 X의 개수를 세기
# A ⊆ X ⊆ A∪B 를 만족하는 X
# X는 {1,2,3,4}를 반드시 포함하고, {5,6}의 부분집합을 선택적으로 추가

count = 0
valid_X = []

# {5, 6}의 모든 부분집합에 대해
from itertools import combinations

for r in range(3):  # 0, 1, 2개 선택
    for subset in combinations([5, 6], r):
        X = A.union(set(subset))
        
        # 조건 1: A ∩ X = A
        if A.intersection(X) == A:
            # 조건 2: X ∪ (A ∪ B) = A ∪ B
            if X.union(A_union_B) == A_union_B:
                count += 1
                valid_X.append(X)

if count == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')