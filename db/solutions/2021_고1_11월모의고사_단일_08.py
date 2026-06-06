import sympy as sp
x, y, a = sp.symbols('x y a')
# 원의 방정식: x^2 + y^2 = 10
# 점 (3, 1)에서의 접선: 3x + y = 10
# 점 (1, a)를 지날 때: 3(1) + a = 10
a_value = 10 - 3*1
print('a =', a_value)
# 검증: 점 (1, 7)이 직선 3x + y = 10 위에 있는가
verify = 3*1 + 7
if verify == 10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')