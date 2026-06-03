import sympy as sp
a = 3
b = 6
# 쌍곡선의 점근선이 y = ±(b/a)x인지 확인
slope = b / a
assert slope == 2, f'Expected slope 2, got {slope}'
print('VERIFY_PASS')