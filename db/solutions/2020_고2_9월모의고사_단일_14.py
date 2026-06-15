import numpy as np
from scipy.optimize import fsolve

# α = arcsin(1/5)
alpha = np.arcsin(1/5)

# n=2인 경우
# 2x = α, π - α
# x = α/2, (π - α)/2
sol_n2 = [alpha/2, (np.pi - alpha)/2]
f2 = sum(sol_n2)

# 검증: sin(2x) = 1/5
for x in sol_n2:
    assert np.isclose(np.sin(2*x), 1/5, atol=1e-10), f'n=2 failed at x={x}'

# n=5인 경우
# 5x = α, π - α, 2π + α, 3π - α, 4π + α, 5π - α
sol_n5_vals = [alpha, np.pi - alpha, 2*np.pi + alpha, 3*np.pi - alpha, 4*np.pi + alpha, 5*np.pi - alpha]
sol_n5 = [val/5 for val in sol_n5_vals]
f5 = sum(sol_n5)

# 검증: sin(5x) = 1/5
for x in sol_n5:
    assert np.isclose(np.sin(5*x), 1/5, atol=1e-10), f'n=5 failed at x={x}'
    assert 0 <= x < np.pi, f'x={x} not in [0, π)'

# 최종 답
answer = f2 + f5
expected = 7*np.pi/2

if np.isclose(answer, expected, atol=1e-10):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')