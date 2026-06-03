import sympy as sp
sin_theta = -4/5
cos_theta = -3/5
sin_neg_theta = -sin_theta
cos_pi_2_plus_theta = -sin_theta
result = sin_neg_theta + cos_pi_2_plus_theta
if abs(result - 8/5) < 1e-10 and cos_theta < 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')