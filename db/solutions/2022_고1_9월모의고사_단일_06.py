a = -4
b = 3

# 경계값 검증: x=a, x=b 에서 |2x+1| = 7 이어야 함
assert abs(2*a + 1) == 7, 'left boundary fail'
assert abs(2*b + 1) == 7, 'right boundary fail'

# 내부점 검증: 중간값은 부등식을 만족해야 함
mid = (a + b) / 2  # x = -0.5
assert abs(2*mid + 1) < 7, 'interior point fail'

# 외부점 검증: 경계 밖은 부등식 불만족
assert abs(2*(a - 1) + 1) >= 7, 'exterior left fail'
assert abs(2*(b + 1) + 1) >= 7, 'exterior right fail'

# ab 계산 확인
ab = a * b
if ab == -12:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')