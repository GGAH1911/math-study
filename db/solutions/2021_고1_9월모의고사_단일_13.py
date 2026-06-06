import sympy as sp
k_vals = [2, 3, 4, 5]
for k in k_vals:
    # 첫 번째 함수와의 교점 판별식
    D1 = 4*k - 7
    # 두 번째 함수와의 교점 판별식
    D2 = 4*k - 24
    assert D1 >= 0, f'k={k}: D1 should be >= 0'
    assert D2 < 0, f'k={k}: D2 should be < 0'
print('VERIFY_PASS')