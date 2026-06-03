import numpy as np

# y = cos(pi/4 * x) 의 주기 검증
# cos(b*x)의 주기 T = 2π/|b| 에서 b = π/4
b = np.pi / 4
T = 2 * np.pi / abs(b)

# T = 8 인지 확인
assert abs(T - 8.0) < 1e-10, f'Period mismatch: {T}'

# 실제로 f(x + T) == f(x) 인지 여러 점에서 확인
for x in np.linspace(-10, 10, 200):
    lhs = np.cos(b * (x + T))
    rhs = np.cos(b * x)
    if abs(lhs - rhs) > 1e-10:
        print('VERIFY_FAIL')
        break
else:
    # T/2 는 주기가 아님을 확인 (최소주기 검증)
    half_T = T / 2
    all_match = all(abs(np.cos(b*(x + half_T)) - np.cos(b*x)) < 1e-10 for x in np.linspace(0.1, 5, 50))
    if all_match:
        print('VERIFY_FAIL')  # T/2도 주기라면 최소주기가 아님
    else:
        print('VERIFY_PASS')
