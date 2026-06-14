import numpy as np

# 두 함수의 주기 비교
a = 6

# f(x) = cos(ax) + 1의 주기
period_f = 2 * np.pi / a

# g(x) = |sin(3x)|의 주기
# sin(3x)의 주기는 2π/3이지만, 절댓값이므로 π/3
period_g = np.pi / 3

# 주기가 같은지 확인
if np.isclose(period_f, period_g):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')