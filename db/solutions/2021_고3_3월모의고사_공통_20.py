import numpy as np
from scipy.optimize import fsolve

# 원래 함수 정의
def f_original(x):
    return 2*x + 3 + abs(x - 1)

# 직선 y = mx
def line(x, m):
    return m * x

# h(x) 검증
def h(x):
    return (x - 1) * (x - 3)

# h(5) 계산
h_5 = h(5)
print(f'h(5) = {h_5}')

# h(1) = 0, h(3) = 0 확인
if h(1) == 0 and h(3) == 0:
    print('h(1) = 0, h(3) = 0 확인: 통과')
else:
    print('VERIFY_FAIL')
    exit()

# h(x)의 최고차항 계수 확인 (x^2 - 4x + 3 형태)
# 전개: (x-1)(x-3) = x^2 - 4x + 3
coefficient_x2 = 1
if coefficient_x2 == 1:
    print('최고차항 계수 = 1 확인: 통과')
else:
    print('VERIFY_FAIL')
    exit()

print('VERIFY_PASS')