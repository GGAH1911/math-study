import numpy as np
a = 1/3
b = np.sqrt(3)
alpha = np.arctan(b)
print(f'Check alpha = pi/3: {np.isclose(alpha, np.pi/3)}')
x1 = alpha / a
x2 = (alpha + np.pi) / a
x4 = (alpha + 3*np.pi) / a
print(f'Check x1 = pi: {np.isclose(x1, np.pi)}')
print(f'Check x4 - x2 = 6pi: {np.isclose(x4 - x2, 6*np.pi)}')
print(f'Check tan(ax1) = b: {np.isclose(np.tan(a*x1), b, atol=1e-10)}')
print(f'Check tan(ax2) = b: {np.isclose(np.tan(a*x2), b, atol=1e-10)}')
print(f'Check tan(ax4) = b: {np.isclose(np.tan(a*x4), b, atol=1e-10)}')
if np.isclose(x1, np.pi) and np.isclose(x4 - x2, 6*np.pi) and np.isclose(np.tan(a*x1), b, atol=1e-10):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')