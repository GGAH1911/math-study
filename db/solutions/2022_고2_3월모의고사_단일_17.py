from sympy import symbols, solve, Poly
import numpy as np

x = symbols('x', real=True)

# 조건 1 검증: a ∈ {-1, 0, 1}
valid_a = []
for a in [-1, 0, 1]:
    # x^2 + 2ax + 1의 판별식
    disc = (2*a)**2 - 4*1*1
    if disc <= 0:  # 모든 x에 대해 >= 0
        valid_a.append(a)

# 조건 2 검증: b ∈ {-2, -1, 0, 1, 2}
valid_b = []
for b in range(-3, 4):
    # x^2 + 2bx + 9의 판별식
    disc = (2*b)**2 - 4*1*9
    if disc < 0:  # 모든 x에 대해 > 0
        valid_b.append(b)

count = len(valid_a) * len(valid_b)

# 샘플 검증: a=0, b=0일 때
# p: x^2 + 1 >= 0 (항상 참)
# ~q: x^2 + 9 > 0 (항상 참)
p_expr = x**2 + 1
q_expr = x**2 + 9

# p가 항상 참인지 확인
p_min = min([float(p_expr.subs(x, val)) for val in np.linspace(-10, 10, 100)])
assert p_min >= 0, f'p is not always >= 0'

# q가 항상 > 0인지 확인
q_min = min([float(q_expr.subs(x, val)) for val in np.linspace(-10, 10, 100)])
assert q_min > 0, f'q is not always > 0'

if count == 15:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')