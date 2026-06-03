import math

# Inverse function: y = (3^x - 1) / 2
x_val = 4
a = (3**x_val - 1) / 2  # should be 40

# Verify: inverse passes through (4, a) <=> original passes through (a, 4)
# i.e. log_3(2*a + 1) == 4
check = math.log(2 * a + 1, 3)

if abs(check - 4) < 1e-9 and a == 40:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
