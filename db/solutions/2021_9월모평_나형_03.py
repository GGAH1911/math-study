import math
cos_pi_6_sq = math.cos(math.pi / 6) ** 2
tan_2pi_3_sq = math.tan(2 * math.pi / 3) ** 2
result = cos_pi_6_sq + tan_2pi_3_sq
expected = 15 / 4
if abs(result - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')