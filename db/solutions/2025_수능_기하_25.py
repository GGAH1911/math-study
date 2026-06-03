import numpy as np
from sympy import symbols, solve, Rational

# 구한 값
a, b, c = 6, 3, 4
A = np.array([a, b, 6])
B = np.array([-4, -2, c])

# 내분점 (3:2)
P = (2*A + 3*B) / 5
print(f'내분점 P: {P}')
assert abs(P[0]) < 1e-10 and abs(P[1]) < 1e-10, '내분점이 z축 위에 있어야 함'

# 외분점 (3:2)
Q = 3*B - 2*A
print(f'외분점 Q: {Q}')
assert abs(Q[2]) < 1e-10, '외분점이 xy평면 위에 있어야 함'

result = a + b + c
assert result == 13, f'결과가 13이어야 하는데 {result}'

print('VERIFY_PASS')