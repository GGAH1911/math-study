import numpy as np

# 원래 조건: alpha + beta = 2, alpha*beta = 4
alpha = 1 + 1j*np.sqrt(3)
beta = 1 - 1j*np.sqrt(3)

n = 6

# 조건 (가): alpha^n + beta^n > 0
alpha_n_plus_beta_n = alpha**n + beta**n
assert alpha_n_plus_beta_n.real > 0, 'Condition (가) failed'

# 조건 (나): alpha^n + beta^n = alpha^(n+1) + beta^(n+1)
alpha_n_plus_1_plus_beta_n_plus_1 = alpha**(n+1) + beta**(n+1)
assert abs(alpha_n_plus_beta_n - alpha_n_plus_1_plus_beta_n_plus_1) < 1e-9, 'Condition (나) failed'

# 원래 방정식 검증
a, b = -2, 4
assert abs(alpha**2 + a*alpha + b) < 1e-9, 'First equation failed for alpha'
assert abs(beta**2 + a*beta + b) < 1e-9, 'First equation failed for beta'
assert abs((alpha+2)**2 + 3*a*(alpha+2) + 3*b) < 1e-9, 'Second equation failed for alpha+2'
assert abs((beta+2)**2 + 3*a*(beta+2) + 3*b) < 1e-9, 'Second equation failed for beta+2'

print('VERIFY_PASS')