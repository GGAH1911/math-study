import numpy as np

def f(x):
    return 2**(-x) + 5

# 구간 [-3, -1]에서 최솟값 수치 탐색
x_vals = np.linspace(-3, -1, 100000)
f_vals = f(x_vals)
numerical_min = np.min(f_vals)

# 우리의 답: 최솟값 = 7 (x = -1에서)
claimed_answer = 7
f_at_endpoint = f(-1.0)

if abs(f_at_endpoint - claimed_answer) < 1e-9 and abs(numerical_min - claimed_answer) < 1e-6:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: f(-1)={f_at_endpoint}, numerical_min={numerical_min}')
