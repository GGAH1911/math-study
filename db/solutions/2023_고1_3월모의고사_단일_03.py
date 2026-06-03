import math
AC = 8 * math.sqrt(3)
angle_A_rad = math.radians(30)
AB = AC * math.cos(angle_A_rad)
BC = AC * math.sin(angle_A_rad)
verify = abs(AB**2 + BC**2 - AC**2) < 1e-10
print('VERIFY_PASS' if verify and abs(AB - 12) < 1e-10 else 'VERIFY_FAIL')