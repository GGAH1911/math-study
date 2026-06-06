import numpy as np
from scipy.optimize import fsolve
import sympy as sp

# 문제의 원래 함수들
def f(x):
    return x**2 - 5*x

def g(x):
    return -0.5*x + 2.5

def line(x, k):
    return x + k

# 주어진 a와 답 검증
p = 3
q = 23/3
pq = p * q

# 범위 내 a 값으로 테스트 (예: a = 5)
a = 5

# a = 5일 때, m + n = 3이 되는 k가 존재하는지 확인
# k = -6을 테스트
k = -6

# x < a에서 f(x)와 line의 교점
# x^2 - 5x = x + k => x^2 - 6x - k = 0
# x^2 - 6x + 6 = 0
discriminant = 36 + 4*k
if discriminant > 0:
    root1 = 3 - np.sqrt(9 + k)
    root2 = 3 + np.sqrt(9 + k)
    m = sum([1 for r in [root1, root2] if r < a])
else:
    m = 0

# x >= a에서 g(x)와 line의 교점
# -0.5*x + 2.5 = x + k => x = (5 - 2k)/3
intersect_x = (5 - 2*k) / 3
n = 1 if intersect_x >= a else 0

result = m + n

if result == 3 and 3 < a < 23/3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')