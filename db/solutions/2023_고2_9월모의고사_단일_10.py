import math

# 주어진 조건
AB = 6
BC = 7
area = 15

# sin(∠ABC) 계산
sin_ABC = 2 * area / (AB * BC)
assert abs(sin_ABC - 5/7) < 1e-10, f'sin(∠ABC) = {sin_ABC}'

# cos(∠ABC) 계산
cos_ABC_squared = 1 - sin_ABC**2
cos_ABC = math.sqrt(cos_ABC_squared)

# 답이 2√6/7인지 확인
expected = 2 * math.sqrt(6) / 7
assert abs(cos_ABC - expected) < 1e-10, f'cos(∠ABC) = {cos_ABC}, expected = {expected}'

# 원래 조건 검증: 넓이
calculated_area = 0.5 * AB * BC * sin_ABC
assert abs(calculated_area - area) < 1e-10, f'area = {calculated_area}, expected = {area}'

# sin² + cos² = 1 검증
trig_check = sin_ABC**2 + cos_ABC**2
assert abs(trig_check - 1.0) < 1e-10, f'sin² + cos² = {trig_check}'

print('VERIFY_PASS')