import math

# 주어진 함수 f(x) = log_3(6x)
# 도함수: f'(x) = 1/(x*ln(3))
# 답: f'(9) = 1/(9*ln(3))

answer_value = 1 / (9 * math.log(3))

# 검증: 수치 미분으로 확인
def f(x):
    return math.log(6*x) / math.log(3)

h = 1e-8
numerical_derivative = (f(9 + h) - f(9 - h)) / (2 * h)

# 해석적 도함수 값
analytical_derivative = 1 / (9 * math.log(3))

if abs(numerical_derivative - analytical_derivative) < 1e-6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')