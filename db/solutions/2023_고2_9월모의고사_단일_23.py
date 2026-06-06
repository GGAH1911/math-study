import math
r = 6
theta = 2 * math.pi / r  # 호의 길이 = r * theta = 2π에서
arc_length = r * theta
area = 0.5 * r**2 * theta
print(f'호의 길이: {arc_length:.6f}, 목표: {2*math.pi:.6f}')
print(f'넓이: {area:.6f}, 목표: {6*math.pi:.6f}')
assert abs(arc_length - 2*math.pi) < 1e-9
assert abs(area - 6*math.pi) < 1e-9
print('VERIFY_PASS')