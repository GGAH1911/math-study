import math

# If problem is sqrt[3](24 * 3^2) = sqrt[3](216)
value = (24 * 9)**(1/3)
if abs(value - 6) < 0.001:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {value} instead of 6')

# Also verify 6^3 = 216
if 6**3 == 216:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')