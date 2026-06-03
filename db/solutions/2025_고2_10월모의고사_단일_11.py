import numpy as np

def inequality_holds(x):
    inner = x**2 - x
    if inner <= 0 or x <= 0:
        return False
    lhs = np.log2(inner)
    log_half_x = -np.log2(x)  # log_{1/2}(x) = -log2(x)
    rhs = 1 - log_half_x
    return bool(lhs < rhs)

alpha, beta = 1, 3
all_pass = True

for x in [1.1, 1.5, 2.0, 2.5, 2.9]:
    if not inequality_holds(x):
        print(f'FAIL: x={x} should satisfy')
        all_pass = False

for x in [0.5, 3.0, 3.5, 10.0]:
    if inequality_holds(x):
        print(f'FAIL: x={x} should NOT satisfy')
        all_pass = False

if not inequality_holds(1.0):
    pass  # x=1 undefined (log(0)), correctly excluded
else:
    print('FAIL: x=1 boundary incorrectly passes')
    all_pass = False

if all_pass and (alpha + beta) == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
