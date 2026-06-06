import sympy as sp
k_vals = [1, 2, 3, 4, 5, 6]
count = 0
for k in k_vals:
    discriminant = 16 * (7 - k)
    if discriminant > 0:
        count += 1
if count == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')