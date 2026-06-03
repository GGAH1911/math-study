import sympy as sp
a = 2
x = sp.Symbol('x')
# 좌극한
left_limit = (a - 2*a)**2
print(f'좌극한: {left_limit}')
# 함수값 (우극한)
right_value = a**2 - 3*a + 6
print(f'함수값: {right_value}')
if left_limit == right_value:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')