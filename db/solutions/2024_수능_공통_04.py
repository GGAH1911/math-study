import sympy as sp
a = 1
left_limit = 3*2 - a
right_limit = 2**2 + a
if left_limit == right_limit:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')