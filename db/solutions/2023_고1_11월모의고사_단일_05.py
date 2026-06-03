import sympy as sp
a_val = 6
b_val = 1
# 원래 원의 중심과 반지름
center_orig = (a_val, -4)
radius = 4
# 평행이동 후 중심
center_after = (a_val + 2, -4 + 5)
# 주어진 최종 원의 중심
center_final = (8, b_val)
# 검증: 중심이 일치하는가?
if center_after == center_final and center_after == (8, 1):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')