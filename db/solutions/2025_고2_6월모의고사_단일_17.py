import math
count = 0
for x in range(0, 24):
    s = math.sin(math.pi * x / 12) - 0.5
    c = math.cos(math.pi * x / 12) - 0.5
    if s * c < -1e-12:
        count += 1
print('VERIFY_PASS' if count == 10 else 'VERIFY_FAIL')