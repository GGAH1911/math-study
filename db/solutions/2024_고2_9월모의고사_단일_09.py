import math

m = 12
base = 1/3

# 원래 함수: y = log_{1/3}(x + m), 정의역 -3 <= x <= 3
# 최댓값 확인

def f(x):
    val = x + m
    if val <= 0:
        return float('-inf')
    return math.log(val) / math.log(base)

# 정의역 내에서 최댓값 수치 탐색
xs = [x * 0.0001 - 3 for x in range(60001)]  # -3 to 3
values = [f(x) for x in xs]
max_val = max(values)

# 최댓값이 -2인지 확인 (오차 1e-4 허용)
if abs(max_val - (-2)) < 1e-4:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: max={max_val}')
