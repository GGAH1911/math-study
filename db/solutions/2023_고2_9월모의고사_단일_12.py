import numpy as np

a = 3
b = 1/4
c = 3*np.pi/4

# 조건 1: 점 (0, -3)이 그래프 위
y_at_0 = a * np.tan(b*0 + c)
if not np.isclose(y_at_0, -3):
    print('VERIFY_FAIL')
    exit()

# 조건 2: 점근선 x = -π
asymptote_1 = b*(-np.pi) + c
if not np.isclose(asymptote_1, np.pi/2):
    print('VERIFY_FAIL')
    exit()

# 조건 3: 점근선 x = -5π
asymptote_2 = b*(-5*np.pi) + c
if not np.isclose(asymptote_2, np.pi/2 - np.pi):
    print('VERIFY_FAIL')
    exit()

# 최종 답
answer = a * b * c
expected = 9/16 * np.pi
if np.isclose(answer, expected):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')