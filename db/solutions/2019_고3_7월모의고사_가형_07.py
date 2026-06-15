from sympy import symbols, solve, Eq, sqrt
a_val = 13
c_val = 5
b_sq = a_val**2 - c_val**2
b_val = sqrt(b_sq)
short_axis = 2 * b_val
if short_axis == 24:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')