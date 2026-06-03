import math

arctan2 = math.atan(2)
limit = 5 * math.pi

count = 0
for k in range(-10, 100):
    x = arctan2 + k * math.pi
    if 0 < x < limit:
        # Verify tan(x) == 2 at this point
        val = math.tan(x)
        assert abs(val - 2) < 1e-9, f'tan({x}) = {val}, expected 2'
        count += 1

expected = 5
if count == expected:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {count}, expected {expected}')
