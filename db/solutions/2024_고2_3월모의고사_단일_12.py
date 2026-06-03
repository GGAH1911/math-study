import sympy as sp
a_vals = [-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4]
count = 0
for a in a_vals:
    slope1, slope2 = a+7, -a+5
    if slope1 > 0 and slope2 > 0:
        count += 1
print('VERIFY_PASS' if count == 11 else 'VERIFY_FAIL')