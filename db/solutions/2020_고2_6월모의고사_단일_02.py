import math
candidate = math.log(2, 4) + math.log(8, 4)
expected = math.log(16, 4)
print('VERIFY_PASS' if math.isclose(candidate, 2.0, rel_tol=1e-9) and math.isclose(expected, 2.0, rel_tol=1e-9) else 'VERIFY_FAIL')