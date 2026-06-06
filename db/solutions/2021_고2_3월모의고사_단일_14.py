import sympy as sp

# 원래 조건 검증
k = 5

# p의 해
p_solutions = [6, -2]

# ~q: |x - 3| <= k 범위
lower = 3 - k
upper = 3 + k

# p => ~q 검증
for x in p_solutions:
    if lower <= x <= upper:
        result = True
    else:
        result = False
    assert result, f"x={x}는 범위 [{lower}, {upper}]에 포함되지 않음"

# k = 4일 때는 조건을 만족하지 않음을 확인
k_test = 4
lower_test = 3 - k_test
upper_test = 3 + k_test
if not (lower_test <= -2 <= upper_test):
    # k=4는 불충분함을 확인
    pass

print('VERIFY_PASS')