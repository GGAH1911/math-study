import numpy as np
alpha = 11 * np.pi / 36
k = np.sin(alpha)
x_A = np.arcsin(k)
x_B = np.pi - np.arcsin(k)
AB = x_B - x_A
x_C = 3*np.pi/2 - alpha
x_D = 3*np.pi/2 + alpha
CD = x_D - x_C
target_y = -np.sqrt(1 - k**2)
cond1 = np.abs(np.sin(x_A) - k) < 1e-10
cond2 = np.abs(np.sin(x_B) - k) < 1e-10
cond3 = np.abs(np.sin(x_C) - target_y) < 1e-10
cond4 = np.abs(np.sin(x_D) - target_y) < 1e-10
cond5 = np.abs(CD - AB - 2*np.pi/9) < 1e-10
cond6 = 0 < k < 1
cond7 = np.abs(AB - 7*np.pi/18) < 1e-10
if cond1 and cond2 and cond3 and cond4 and cond5 and cond6 and cond7:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')