import math
t = math.pi / 3
dxdt = 1 + math.cos(t)
dydt = 4 * math.sin(t) + 4 * math.sin(t) * math.cos(t)
dydx = dydt / dxdt
expected = 2 * math.sqrt(3)
if abs(dydx - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {dydx}, expected {expected}')