import math
AB = 3
BC = math.sqrt(7)
AC = math.sqrt(AB**2 + BC**2)
cos_A = AB / AC
expected = 3/4
print('VERIFY_PASS' if abs(cos_A - expected) < 1e-9 else 'VERIFY_FAIL')