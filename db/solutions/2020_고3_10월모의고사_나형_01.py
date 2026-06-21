import math
from fractions import Fraction

# log_2(√8) 계산
result = math.log2(math.sqrt(8))
expected = 3/2

if math.isclose(result, expected, rel_tol=1e-9):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')