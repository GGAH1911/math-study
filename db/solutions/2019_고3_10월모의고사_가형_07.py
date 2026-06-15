import math
t = math.pi / 3
dx = 2 + math.cos(t)
dy = math.sin(t)
speed = math.sqrt(dx**2 + dy**2)
expected = math.sqrt(7)
if math.isclose(speed, expected, rel_tol=1e-9):
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {speed}, expected {expected}')