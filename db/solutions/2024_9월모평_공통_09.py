import numpy as np

# 원래 부등식: cos(x) <= sin(pi/7),  0 <= x <= 2*pi
# 해의 범위가 alpha <= x <= beta 임을 수치로 검증

alpha = 5 * np.pi / 14
beta  = 23 * np.pi / 14
threshold = np.sin(np.pi / 7)

# 범위 내 모든 점이 부등식을 만족하는지
xs_in = np.linspace(alpha, beta, 100000)
xs_out_left  = np.linspace(0, alpha - 1e-9, 50000)
xs_out_right = np.linspace(beta + 1e-9, 2*np.pi, 50000)

cond_in        = np.all(np.cos(xs_in) <= threshold + 1e-9)
cond_out_left  = np.all(np.cos(xs_out_left)  > threshold - 1e-9)
cond_out_right = np.all(np.cos(xs_out_right) > threshold - 1e-9)

beta_minus_alpha = beta - alpha  # should be 9*pi/7
check_value = np.isclose(beta_minus_alpha, 9*np.pi/7, atol=1e-10)

if cond_in and cond_out_left and cond_out_right and check_value:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'cond_in={cond_in}, cond_out_left={cond_out_left}, cond_out_right={cond_out_right}, check_value={check_value}')
