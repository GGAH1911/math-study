import math

# 삼각함수 값 계산
sin_val = math.sin(2 * math.pi / 3)
tan_val = math.tan(7 * math.pi / 6)

# 원래 식 계산
result = (10 * sin_val) / tan_val

# 정답 검증
if abs(result - 15) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')