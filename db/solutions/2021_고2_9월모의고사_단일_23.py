import math
from scipy.optimize import minimize_scalar

# 정의역
x_min, x_max = -4, -2

# 함수 정의
def f(x):
    return (1/3)**x + 1

# 정의역 내 최댓값 찾기
result_min = minimize_scalar(lambda x: f(x), bounds=(x_min, x_max), method='bounded')
min_val = f(result_min.x)
max_val = max(f(x_min), f(x_max))

# 양 끝점에서의 값
f_at_minus4 = f(-4)
f_at_minus2 = f(-2)

# 검증
expected_answer = 82
if abs(f_at_minus4 - expected_answer) < 1e-9 and f_at_minus4 >= f_at_minus2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')