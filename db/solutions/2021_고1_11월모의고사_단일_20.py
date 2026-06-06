# 조건 확인
X = {1, 2, 3, 6, 7, 8}
A = {1, 2, 3, 4, 5}
B = {3, 4, 5, 6, 7}

# (가) n(X) = 6
assert len(X) == 6, f'n(X) = {len(X)}'

# (나) A - X = B - X
A_minus_X = A - X
B_minus_X = B - X
assert A_minus_X == B_minus_X, f'A-X={A_minus_X}, B-X={B_minus_X}'

# (다) (X-A) ∩ (X-B) ≠ ∅
X_minus_A = X - A
X_minus_B = X - B
intersection = X_minus_A & X_minus_B
assert len(intersection) > 0, f'intersection={intersection}'

# 최솟값 확인
total = sum(X)
assert total == 27, f'sum={total}'

print('VERIFY_PASS')