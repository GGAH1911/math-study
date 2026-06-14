CANDIDATE = 10

from itertools import product

# 복원추출: 가능한 모든 (a, b) 쌍
outcomes = list(product([1, 2, 3, 4], repeat=2))
n = len(outcomes)  # 16

# X = a - b
X_vals = [a - b for a, b in outcomes]

# E(X)
E_X = sum(X_vals) / n

# E(X^2)
E_X2 = sum(x**2 for x in X_vals) / n

# V(X) = E(X^2) - [E(X)]^2
V_X = E_X2 - E_X**2

# V(Y) = V(2X+1) = 4*V(X)
V_Y = 4 * V_X

if abs(V_Y - CANDIDATE) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: V(Y) = {V_Y}, CANDIDATE = {CANDIDATE}')
