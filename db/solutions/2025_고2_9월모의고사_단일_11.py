import math
a, b = 1, -2
# f(x) = log_2(x+a) + b
def f(x):
    return math.log2(x + a) + b

# 검증: 그래프의 두 점
assert abs(f(3) - 0) < 1e-9, f'f(3) = {f(3)}, expected 0'
assert abs(f(0) - (-2)) < 1e-9, f'f(0) = {f(0)}, expected -2'

# 최종 답
result = f(15)
assert abs(result - 2) < 1e-9, f'f(15) = {result}, expected 2'
print('VERIFY_PASS')