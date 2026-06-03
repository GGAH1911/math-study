import math
x = math.pi/6
lhs = 2*math.sin(x) - 1
in_range = (-math.pi/2 < x < math.pi/2)
print('VERIFY_PASS' if abs(lhs) < 1e-12 and in_range else 'VERIFY_FAIL')
