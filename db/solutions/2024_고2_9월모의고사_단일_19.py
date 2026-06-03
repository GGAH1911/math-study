import numpy as np

t = 3**0.5  # t = sqrt(3)

def f(x):
    return 3 * np.sin(np.pi / 2 * x)

beta = np.arcsin(t / 3)

x_A = 2 + 2*beta/np.pi
x_B = 6 + 2*beta/np.pi
x_C = 4 + 2*beta/np.pi

y_A = -t
y_B = -t
y_C = f(x_C)

# Check A, B on curve and line y=-t
cond1 = abs(f(x_A) - (-t)) < 1e-9
cond2 = abs(f(x_B) - (-t)) < 1e-9
# Check C on curve
cond3 = abs(y_C - t) < 1e-9  # f(x_C) should equal t
# Check domain
cond4 = (0 <= x_A <= 7) and (0 <= x_B <= 7) and (0 <= x_C <= 7)
# Check 0 < t < 3
cond5 = 0 < t < 3

AB = np.sqrt((x_B - x_A)**2 + (y_B - y_A)**2)
AC = np.sqrt((x_C - x_A)**2 + (y_C - y_A)**2)
BC = np.sqrt((x_C - x_B)**2 + (y_C - y_B)**2)

side_ok = abs(AB - 4) < 1e-8 and abs(AC - 4) < 1e-8 and abs(BC - 4) < 1e-8

if cond1 and cond2 and cond3 and cond4 and cond5 and side_ok:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: AB={AB:.6f}, AC={AC:.6f}, BC={BC:.6f}, conds={cond1,cond2,cond3,cond4,cond5}')
