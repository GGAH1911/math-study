import math
CANDIDATE = math.sqrt(3) / 2
result = math.cos(13 * math.pi / 6)
if math.isclose(result, CANDIDATE, rel_tol=1e-9):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')