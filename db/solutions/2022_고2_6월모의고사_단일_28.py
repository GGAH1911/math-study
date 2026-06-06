import math

AB = 9/2
BC = 6
angle_ABC = math.pi / 3

AC_squared = AB**2 + BC**2 - 2*AB*BC*math.cos(angle_ABC)
AC = math.sqrt(AC_squared)

ratio = AC / AB
expected_ratio = math.sqrt(13) / 3

if abs(ratio - expected_ratio) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')