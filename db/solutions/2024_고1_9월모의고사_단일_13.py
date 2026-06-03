import math
k = 1/2
x0, y0 = 0, 0
x1, y1 = 1, 3
dist = abs(k*x0 - y0 + (3 - k)) / math.sqrt(k**2 + 1)
result = 'VERIFY_PASS' if abs(dist - math.sqrt(5)) < 1e-10 else 'VERIFY_FAIL'
print(result)