import math
tan_alpha = 2/3
tan_beta = 1/5
tan_sum = (tan_alpha + tan_beta) / (1 - tan_alpha * tan_beta)
if abs(tan_sum - 1.0) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')