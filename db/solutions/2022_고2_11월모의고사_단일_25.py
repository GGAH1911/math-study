import math

# 답: r = 6
r = 6

# 검증 1: 호 AC의 길이 = π
# 호 AC의 중심각 = π/r = π/6
angle_AOC = math.pi / r
len_AC = r * angle_AOC
assert abs(len_AC - math.pi) < 1e-9, f'호 AC 길이 불일치: {len_AC}'

# 검증 2: 부채꼴 OBC의 넓이 = 15π
# 호 BC의 중심각 = π - π/r = 5π/6
angle_BOC = math.pi - angle_AOC
area_OBC = 0.5 * r**2 * angle_BOC
expected_area = 15 * math.pi
assert abs(area_OBC - expected_area) < 1e-9, f'부채꼴 OBC 넓이 불일치: {area_OBC} vs {expected_area}'

print('VERIFY_PASS')