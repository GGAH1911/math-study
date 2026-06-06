import numpy as np
a_squared = 2
a = np.sqrt(a_squared)
x_vals = [1/4, 5/4, 9/4]
y_f = [a * np.sin(np.pi * x) for x in x_vals]
y_g = [a * np.cos(np.pi * x) for x in x_vals]
for i in range(3):
    assert np.isclose(y_f[i], y_g[i]), f'교점 확인 실패: {i}'
x1, x2, x3 = x_vals
y1, y2, y3 = y_f
area = 0.5 * abs(x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2))
if np.isclose(area, 2):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')