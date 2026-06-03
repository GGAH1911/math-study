import numpy as np

a = np.pi / 3
dom_end = 4 * np.pi / a  # = 12

x_sols = []

# Case 1: sin(t)=0, t=k*pi
for k in range(20):
    t = k * np.pi
    if t < -np.pi/3: continue
    x = (t + np.pi/3) / a
    if 0 <= x < dom_end:
        x_sols.append(x)

# Case 2: sin(t)=-1, t = 3pi/2 + 2m*pi
for m in range(20):
    t = 3*np.pi/2 + 2*m*np.pi
    if t < -np.pi/3: continue
    x = (t + np.pi/3) / a
    if 0 <= x < dom_end:
        x_sols.append(x)

x_sols.sort()
n = len(x_sols)
s = sum(x_sols)

all_ok = all(np.isclose(abs(4*np.sin(a*x - np.pi/3) + 2), 2, atol=1e-9) for x in x_sols)

if n == 6 and np.isclose(s, 39, atol=1e-9) and all_ok and np.isclose(n * a, 2*np.pi, atol=1e-9):
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: n={n}, sum={s:.6f}, n*a={n*a:.6f}, all_ok={all_ok}')
