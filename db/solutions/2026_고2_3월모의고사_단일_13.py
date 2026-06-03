import cmath
z = -1 + 1j
z_bar = -1 - 1j
condition = z * z_bar + 2*z
if abs(condition - 2j) < 1e-9:
    z_squared = z**2
    if abs(z_squared - (-2j)) < 1e-9:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')