CANDIDATE = 121

# 주어진 조건들을 확인
from sympy import symbols, solve, Eq

a, b, c, d = symbols('a b c d', real=True, positive=True)

# 조건식들
eq1 = Eq(a + b + c + d, 1)  # 확률의 합
eq2 = Eq(1*a + 2*b + 3*c + 4*d, 2)  # E(X) = 2
eq3 = Eq(1**2*a + 2**2*b + 3**2*c + 4**2*d, 5)  # E(X^2) = 5

# 조건을 만족하는 한 조해: a=1/2, b=0, c=1/2, d=0
probs = {a: 0.5, b: 0, c: 0.5, d: 0}

# E(X) 확인
EX = sum([x_val * probs[prob] for x_val, prob in [(1,a), (2,b), (3,c), (4,d)]])
assert abs(EX - 2) < 1e-10, f'E(X) check failed: {EX}'

# E(X^2) 확인
EX2 = sum([x_val**2 * probs[prob] for x_val, prob in [(1,a), (2,b), (3,c), (4,d)]])
assert abs(EX2 - 5) < 1e-10, f'E(X^2) check failed: {EX2}'

# V(X) 계산
VX = EX2 - EX**2
assert abs(VX - 1) < 1e-10, f'V(X) check failed: {VX}'

# Y = 10X + 1 의 관계에서
# E(Y) = 10*E(X) + 1
EY = 10 * EX + 1
assert abs(EY - 21) < 1e-10, f'E(Y) calculation error'

# V(Y) = 100 * V(X)
VY = 100 * VX
assert abs(VY - 100) < 1e-10, f'V(Y) calculation error'

# 최종 답
result = EY + VY
assert abs(result - CANDIDATE) < 1e-10, f'Final answer mismatch: {result} != {CANDIDATE}'

print('VERIFY_PASS')