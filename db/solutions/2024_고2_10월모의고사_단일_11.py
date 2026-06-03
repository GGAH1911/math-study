import math
from sympy import cos as sym_cos, sin as sym_sin, tan as sym_tan, pi, sqrt, simplify, symbols, solve

theta = symbols('theta', real=True)
cos_theta = -1/3

sin_squared = 1 - cos_theta**2
sin_theta_val = sqrt(sin_squared)

cos_lhs = -sin_theta_val
tan_theta_val = sin_theta_val / cos_theta
result = cos_lhs * tan_theta_val
result_simplified = simplify(result)

if abs(float(result_simplified) - 8/3) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')