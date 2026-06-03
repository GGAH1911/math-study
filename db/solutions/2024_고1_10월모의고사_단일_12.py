# 조건 검증
n_C = 8
n_B_minus_C = n_C / 2  # = 4

# 조건 (나) 검증: n(C) = 2 * n(B - C)
assert n_C == 2 * n_B_minus_C, f'조건 (나) 실패: {n_C} != 2*{n_B_minus_C}'

# n(B ∪ C) = 12 검증
# n(B ∪ C) = n(B - C) + n(C)
n_B_union_C = n_B_minus_C + n_C
assert n_B_union_C == 12, f'n(B ∪ C) 실패: {n_B_union_C} != 12'

print('VERIFY_PASS')