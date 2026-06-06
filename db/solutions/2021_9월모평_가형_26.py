import sympy as sp
from sympy import symbols, E, simplify

# X와 Y의 확률 계산
# Y = 10X + 1 관계를 확인하고
# E(X) = 2, V(X) = 1임을 이용

# E(X) = 2, E(X²) = 5 조건 확인
E_X = 2
E_X2 = 5
V_X = E_X2 - E_X**2

assert V_X == 1, f'V(X) should be 1, got {V_X}'
assert E_X == 2, f'E(X) should be 2, got {E_X}'

# Y = 10X + 1의 기댓값과 분산
E_Y = 10 * E_X + 1
V_Y = 100 * V_X

assert E_Y == 21, f'E(Y) should be 21, got {E_Y}'
assert V_Y == 100, f'V(Y) should be 100, got {V_Y}'

result = E_Y + V_Y
assert result == 121, f'E(Y) + V(Y) should be 121, got {result}'

print('VERIFY_PASS')