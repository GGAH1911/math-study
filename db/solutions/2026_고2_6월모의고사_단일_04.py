import math
x = 4 * math.pi / 3
result = 2 * math.sin(x) + math.sqrt(3)
is_in_domain = (math.pi/2 <= x <= 3*math.pi/2)
print('VERIFY_PASS' if abs(result) < 1e-10 and is_in_domain else 'VERIFY_FAIL')