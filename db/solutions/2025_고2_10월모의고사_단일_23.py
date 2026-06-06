import math

# 문제에서 주어진 조건
theta = 2 * math.pi / 5  # 중심각
l_given = 4 * math.pi     # 호의 길이

# 답: a = 20이면 넓이 = 20π
a = 20
S_answer = a * math.pi

# 호의 길이와 부채꼴 넓이 공식으로부터 반지름 구하기
# l = r*theta => r = l/theta
r = l_given / theta

# 부채꼴 넓이: S = (1/2)*r^2*theta
S_calc = 0.5 * r**2 * theta

# 검증: 계산된 넓이와 답이 일치하는가?
if abs(S_calc - S_answer) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')