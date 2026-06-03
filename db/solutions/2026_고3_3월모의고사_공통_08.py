import math
from decimal import Decimal, getcontext
getcontext().prec = 50

cos_theta = -4 * math.sqrt(17) / 17
sin_theta = cos_theta / 4

verify1 = math.isclose(sin_theta**2 + cos_theta**2, 1, rel_tol=1e-9)
verify2 = math.isclose(cos_theta, 4 * sin_theta, rel_tol=1e-9)
verify3 = cos_theta < 0
sin_half_pi_plus_theta = cos_theta
verify4 = sin_half_pi_plus_theta < 0

if verify1 and verify2 and verify3 and verify4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')