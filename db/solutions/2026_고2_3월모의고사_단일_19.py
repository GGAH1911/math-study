from sympy import symbols, solve

# 경우 2-2 검증: A∩B = {7, 10}, B-A = {3, 4, 5}
A_cap_B = {7, 10}
B_minus_A = {3, 4, 5}
A = {6, 7, 8, 10}  # 최소 집합
B = {3, 4, 5, 7, 10}

# 조건 (가) 검증
assert len(A_cap_B) == 2
assert len(B_minus_A) == 3

# 조건 (나) 검증: p ∈ A∩B이면 (p+2)/3 ∈ B-A
for p in A_cap_B:
    val = (p + 2) / 3
    assert val in B_minus_A, f'{p}에 대해 실패'

# 조건 (다) 검증: q ∈ B-A이면 q+3 ∈ A
for q in B_minus_A:
    assert q + 3 in A, f'{q}에 대해 실패'

# B-A의 합
sum_B_minus_A = sum(B_minus_A)
assert sum_B_minus_A == 12

print('VERIFY_PASS')