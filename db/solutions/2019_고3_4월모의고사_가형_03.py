import sympy as sp
a_squared = 16
b_squared = 7
a = sp.sqrt(a_squared)
candidate = 8
major_axis_length = 2 * a
if sp.simplify(major_axis_length - candidate) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')