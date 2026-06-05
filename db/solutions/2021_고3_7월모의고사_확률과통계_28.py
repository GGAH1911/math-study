import math

def phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))

# Derived values
m = 6
sigma = 6
a = 12

# Check (가): a = 2m, sigma^2 = 36
assert abs(a - 2*m) < 1e-9, 'a != 2m'
assert abs(sigma**2 - 36) < 1e-9, 'sigma^2 != 36'

# Check (나): P(X<=4) == P(Y>=a)
P_X_le_4 = phi((4 - m) / 2)          # P(Z <= -1)
P_Y_ge_a = 1 - phi((a - m) / sigma)  # P(Z >= 1)
assert abs(P_X_le_4 - P_Y_ge_a) < 1e-9, f'(나) fail: {P_X_le_4} vs {P_Y_ge_a}'

# P(Y >= 9)
P_Y_ge_9 = 1 - phi((9 - m) / sigma)  # P(Z >= 0.5)
# Table value: P(0<=Z<=0.5)=0.1915 => 0.5-0.1915=0.3085
expected = 0.3085

if abs(P_Y_ge_9 - expected) < 0.0001:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: P(Y>=9)={P_Y_ge_9:.4f}, expected={expected}')
