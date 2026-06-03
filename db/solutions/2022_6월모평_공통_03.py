import math

# 주어진 조건
tan_theta = 12/5

# sin과 cos 구하기
# tan = sin/cos = 12/5
# sin^2 + cos^2 = 1
# sin = (12/5)cos를 대입하면
# (144/25)cos^2 + cos^2 = 1
# (169/25)cos^2 = 1
# cos^2 = 25/169
# 3사분면이므로 cos < 0
cos_theta = -5/13
sin_theta = -12/13

# 검증: tan 확인
tan_check = sin_theta / cos_theta
assert abs(tan_check - 12/5) < 1e-9, f'tan 검증 실패: {tan_check}'

# 검증: sin^2 + cos^2 = 1
identity_check = sin_theta**2 + cos_theta**2
assert abs(identity_check - 1.0) < 1e-9, f'기본 항등식 검증 실패: {identity_check}'

# 최종 답
answer = sin_theta + cos_theta
expected = -17/13

assert abs(answer - expected) < 1e-9, f'답 검증 실패: {answer} vs {expected}'

print('VERIFY_PASS')