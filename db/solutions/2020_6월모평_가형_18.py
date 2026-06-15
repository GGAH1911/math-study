import numpy as np

def compute_f(a_val):
    # Q = (3cos t, 3sin t), t in [0, pi/2]
    # |OP + OQ|^2 = (1 + 3cos t)^2 + (a + 3sin t)^2
    t = np.linspace(0, np.pi/2, 200001)
    vals = (1.0 + 3.0*np.cos(t))**2 + (a_val + 3.0*np.sin(t))**2
    return float(np.sqrt(np.max(vals)))

a1 = np.sqrt(3.0)
a2 = -3.0

f1 = compute_f(a1)
f2 = compute_f(a2)
product = a1 * a2
expected_product = -3.0 * np.sqrt(3.0)

cond1 = abs(f1 - 5.0) < 1e-4
cond2 = abs(f2 - 5.0) < 1e-4
cond3 = abs(product - expected_product) < 1e-9

if cond1 and cond2 and cond3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    if not cond1: print(f'f(sqrt3)={f1}, expected 5')
    if not cond2: print(f'f(-3)={f2}, expected 5')
    if not cond3: print(f'product={product}, expected {expected_product}')
