import numpy as np
from scipy.optimize import fsolve

# Setup
vec_b = np.array([6, 0])
vec_c = np.array([4.5, 3*np.sqrt(3)/2])
vec_d = np.array([1.5, -3*np.sqrt(3)/2])

# Verify given conditions
assert np.isclose(np.dot(vec_b, vec_c), 27), 'Condition AB·AC=27 failed'
assert np.isclose(np.dot(vec_b, vec_d), 9), 'Condition AB·AD=9 failed'
assert np.isclose(np.dot(vec_c, vec_d), 0), 'Orthogonality failed'

# Verify condition (나)
lambda_p = 2/3
mu_q = 1/3
vec_aq = mu_q * vec_c
vec_ap = lambda_p * vec_c

vec_qb = vec_b - vec_aq
vec_qd = vec_d - vec_aq
dot_qb_qd = np.dot(vec_qb, vec_qd)
assert np.isclose(dot_qb_qd, 3), f'Condition (나) failed: got {dot_qb_qd}'

# Verify condition (가)
k = 5/2
vec_dp = vec_ap - vec_d
vec_bc = vec_c - vec_b

lhs = 1.5 * vec_dp - vec_b
rhs = k * vec_bc
assert np.allclose(lhs, rhs, atol=1e-10), f'Condition (가) failed: lhs={lhs}, rhs={rhs}'

# Calculate answer
vec_aq_dot_vec_dp = np.dot(vec_aq, vec_dp)
result = k * vec_aq_dot_vec_dp

assert np.isclose(result, 15), f'Final answer verification failed: got {result}'
print('VERIFY_PASS')