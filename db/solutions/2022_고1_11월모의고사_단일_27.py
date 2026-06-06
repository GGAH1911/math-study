from itertools import permutations

# 함수 정의
f_map = {-2: -1, -1: 0, 0: 2, 1: 1, 2: -2}

# 역함수 계산
f_inv_map = {v: k for k, v in f_map.items()}

# 조건 (가) 검증: (f∘f)(-1) + f^(-1)(-2) = 4
composition_val = f_map[f_map[-1]]  # f(f(-1))
inv_val = f_inv_map[-2]  # f^(-1)(-2)
check_a = composition_val + inv_val
assert check_a == 4, f"조건 (가) 실패: {composition_val} + {inv_val} = {check_a}"

# 조건 (나) 검증: k=0,1일 때 f(k)×f(k-2) ≤ 0
for k in [0, 1]:
    product = f_map[k] * f_map[k-2]
    assert product <= 0, f"조건 (나) 실패 (k={k}): {f_map[k]} × {f_map[k-2]} = {product}"

# 일대일 대응 검증
assert len(set(f_map.values())) == 5, "일대일 대응 실패"

# 최종 답 계산
answer = 6 * f_map[0] + 5 * f_map[1] + 2 * f_map[2]
assert answer == 13, f"답 계산 오류: {answer}"

print('VERIFY_PASS')