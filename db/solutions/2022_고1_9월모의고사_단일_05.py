import numpy as np
from sympy import symbols, solve, Rational

# 두 점 A, B
A = np.array([-4, 0])
B = np.array([5, 3])

# 2:1로 내분하는 점
# 내분점 = (n*A + m*B) / (m+n) where m=2, n=1
m, n = 2, 1
P = (n * A + m * B) / (m + n)

a, b = P[0], P[1]

# 검증: P가 실제로 AB를 2:1로 내분하는지 확인
# AP : PB = 2 : 1이어야 함
AP = np.linalg.norm(P - A)
PB = np.linalg.norm(B - P)
ratio = AP / PB if PB != 0 else float('inf')

# a + b 계산
result = a + b

# 검증
assert abs(a - 2.0) < 1e-9, f'a should be 2, got {a}'
assert abs(b - 2.0) < 1e-9, f'b should be 2, got {b}'
assert abs(ratio - 2.0) < 1e-9, f'Ratio AP:PB should be 2:1, got {ratio}'
assert abs(result - 4.0) < 1e-9, f'a+b should be 4, got {result}'

print('VERIFY_PASS')