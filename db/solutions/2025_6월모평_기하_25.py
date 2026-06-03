import math

a = (-3, 3)
b = (1, -1)

# |b|
magnitude_b = math.sqrt(b[0]**2 + b[1]**2)
assert abs(magnitude_b - math.sqrt(2)) < 1e-9

# Distance from b to center a
dist_b_to_a = math.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)
assert abs(dist_b_to_a - 4*math.sqrt(2)) < 1e-9

# Radius of circle
radius = magnitude_b

# Minimum distance from b to circle
min_distance = dist_b_to_a - radius
expected_answer = 3 * math.sqrt(2)

if abs(min_distance - expected_answer) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')