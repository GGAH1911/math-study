import numpy as np

def x_func(t):
    return np.exp(4*t) * (1 + np.sin(np.pi*t)**2)

def y_func(t):
    return np.exp(4*t) * (1 - 3*np.cos(np.pi*t)**2)

t = 1/4
e = np.e

x_val = x_func(t)
y_val = y_func(t)
line_y = 3*x_val - 5*e

on_line = np.isclose(y_val, line_y, atol=1e-9)

h = 1e-8
dx_dt = (x_func(t+h) - x_func(t-h)) / (2*h)
dy_dt = (y_func(t+h) - y_func(t-h)) / (2*h)
slope_numerical = dy_dt / dx_dt
slope_expected = (3*np.pi - 2) / (np.pi + 6)

slope_ok = np.isclose(slope_numerical, slope_expected, rtol=1e-6)

if on_line and slope_ok:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'on_line={on_line}, y_val={y_val:.6f}, line_y={line_y:.6f}')
    print(f'slope_ok={slope_ok}, numerical={slope_numerical:.8f}, expected={slope_expected:.8f}')
