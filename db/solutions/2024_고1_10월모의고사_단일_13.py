from itertools import combinations

A = {1, 3, 4}
k = 5

# B 계산
B = set()
for x in A:
    B.add((x + k) / 2)

# A ∩ B 계산
A_cap_B = A & B

# (A ∩ B) ⊂ X ⊂ A 를 만족하는 X의 개수 계산
# X는 A의 부분집합이면서 A∩B를 포함해야 함
# A \ (A∩B)의 각 부분집합과 A∩B의 합집합이 X

A_minus_B = A - B
X_count = 2 ** len(A_minus_B)

if X_count == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')