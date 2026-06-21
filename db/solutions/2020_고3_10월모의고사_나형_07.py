import numpy as np
from scipy.optimize import fsolve

def f1(x):
    return np.sin(x)

def f2(x):
    return np.cos(x + np.pi/2) + 1

def equation(x):
    return f1(x) - f2(x)

# 0 <= x < 2π 범위에서 교점 찾기
x_range = np.linspace(0, 2*np.pi - 0.001, 100)
y1 = f1(x_range)
y2 = f2(x_range)

# 부호 변화를 찾아서 정확한 근 구하기
roots = []
for i in range(len(x_range) - 1):
    if equation(x_range[i]) * equation(x_range[i+1]) < 0:
        root = fsolve(equation, x_range[i])[0]
        if 0 <= root < 2*np.pi and not any(abs(root - r) < 1e-6 for r in roots):
            roots.append(root)

roots.sort()
sum_x = sum(roots)

# π와의 비교
pi = np.pi
if abs(sum_x - pi) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')