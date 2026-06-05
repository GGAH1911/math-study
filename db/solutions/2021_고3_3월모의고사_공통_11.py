import math

# 문제 데이터
angle_AOB = 5 * math.pi / 6
r = 3

# sin(5π/6) = 1/2
sin_5pi6 = math.sin(angle_AOB)
assert abs(sin_5pi6 - 0.5) < 1e-9

# 부채꼴 넓이: (1/2)r²θ
sector_area = 0.5 * r**2 * angle_AOB
expected_sector = 15 * math.pi / 4
assert abs(sector_area - expected_sector) < 1e-9

# 삼각형 OAB 넓이: (1/2)r²sin(θ)
triangle_area = 0.5 * r * r * sin_5pi6
expected_triangle = 9 / 4
assert abs(triangle_area - expected_triangle) < 1e-9

# 렌즈 하나: 부채꼴 - 삼각형
lens_one = sector_area - triangle_area
expected_lens_one = (15 * math.pi - 9) / 4
assert abs(lens_one - expected_lens_one) < 1e-9

# 두 원의 교집합 (대칭)
intersection = 2 * lens_one
expected_intersection = (15 * math.pi - 9) / 2
assert abs(intersection - expected_intersection) < 1e-9

# S₁: 원O'의 넓이 - 교집합
circ_area = math.pi * r**2
S1 = circ_area - intersection
expected_S1 = (3 * math.pi + 9) / 2
assert abs(S1 - expected_S1) < 1e-9

# 마름모의 대각선
cos_5pi12 = math.cos(5 * math.pi / 12)
sin_5pi12 = math.sin(5 * math.pi / 12)

OO_prime = 6 * cos_5pi12
AB = 6 * sin_5pi12

# S₂: 마름모 넓이 = (1/2)d₁d₂
S2 = 0.5 * OO_prime * AB
expected_S2 = 9 * sin_5pi6
assert abs(S2 - expected_S2) < 1e-9
assert abs(S2 - 9/2) < 1e-9

# S₁ - S₂
result = S1 - S2
expected_result = 3 * math.pi / 2
assert abs(result - expected_result) < 1e-9

print('VERIFY_PASS')