import math
CANDIDATE = 3
result = math.log2(3) + math.log2(8/3)
print('VERIFY_PASS' if math.isclose(result, CANDIDATE, rel_tol=1e-9) else 'VERIFY_FAIL')