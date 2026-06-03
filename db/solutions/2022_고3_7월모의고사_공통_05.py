import sympy as sp
a_val = 3
x = sp.Symbol('x')
# 좌극한
left_limit = 2 - 1
# 우극한 (x=2에서 f(2))
right_limit = 2**2 - a_val*2 + 3
if abs(left_limit - right_limit) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')