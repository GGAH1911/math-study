import sympy as sp
# 포물선 x^2 = 8y의 초점과 준선
# 표준형 x^2 = 4py에서 4p = 8, p = 2
p = 2
focus_y = p
directrix_y = -p
distance = focus_y - directrix_y
assert distance == 4, f'Expected 4, got {distance}'
print('VERIFY_PASS')