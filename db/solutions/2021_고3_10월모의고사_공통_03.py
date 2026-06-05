import numpy as np

def f(x):
    return np.tan(np.pi * x + np.pi / 2)

period = 1  # 우리의 답

# tan이 정의되는 점(분모≠0)에서 f(x+T) = f(x) 확인
test_points = [0.1, 0.15, 0.3, 0.7, 0.85]
pass_period = True
for x in test_points:
    v1 = f(x)
    v2 = f(x + period)
    if not np.isclose(v1, v2, atol=1e-9):
        pass_period = False
        break

# period=0.5는 성립하지 않음을 확인(최소주기임을 검증)
fail_half = False
for x in [0.1, 0.2, 0.3]:
    if not np.isclose(f(x), f(x + 0.5), atol=1e-9):
        fail_half = True
        break

if pass_period and fail_half:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
