import math
a = -2
b = -4
# 곡선: y = 2^(x-a) + b
# 원점을 지나는가?
y_at_origin = 2**(0 - a) + b
assert abs(y_at_origin - 0) < 1e-10, f'원점 조건 실패: y(0) = {y_at_origin}'
# 점근선이 y = -4인가? (x -> -infinity일 때)
# x가 매우 작을 때 2^(x-a)는 0에 가까워지므로 y는 b에 가까워짐
assert abs(b - (-4)) < 1e-10, f'점근선 조건 실패: b = {b}'
print('VERIFY_PASS')