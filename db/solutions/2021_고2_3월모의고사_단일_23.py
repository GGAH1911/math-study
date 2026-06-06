import math

# 원래 함수 f(x) = sqrt(x-2) + 2
def f(x):
    return math.sqrt(x - 2) + 2

# 답: f^(-1)(7) = 27
answer = 27

# 검증: f(27) = 7인지 확인
result = f(answer)

if abs(result - 7) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')