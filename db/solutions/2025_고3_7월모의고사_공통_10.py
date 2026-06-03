import numpy as np

def f(x):
    if 0 <= x < 1:
        return 3 * np.sin(np.pi * x) + 4
    elif 1 <= x < 2:
        return 9 * np.sin(np.pi * x) + 4
    return None

points = []

# 구간 1: [0, 1)
points.append((0.0, 4))  # y=4
alpha = np.arcsin(1/3)
points.append((alpha/np.pi, 5))  # y=5
points.append(((np.pi-alpha)/np.pi, 5))
alpha = np.arcsin(2/3)
points.append((alpha/np.pi, 6))  # y=6
points.append(((np.pi-alpha)/np.pi, 6))
points.append((0.5, 7))  # y=7

# 구간 2: [1, 2)
points.append((1.0, 4))  # y=4
alpha = np.arcsin(1/9)
points.append((1 + alpha/np.pi, 3))  # y=3
points.append((2 - alpha/np.pi, 3))
alpha = np.arcsin(2/9)
points.append((1 + alpha/np.pi, 2))  # y=2
points.append((2 - alpha/np.pi, 2))
alpha = np.arcsin(1/3)
points.append((1 + alpha/np.pi, 1))  # y=1
points.append((2 - alpha/np.pi, 1))

verified = True
for x, y in points:
    fx = f(x)
    if abs(fx - y) > 1e-10:
        verified = False
        break

if len(points) == 13 and verified:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')