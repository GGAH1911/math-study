import sympy as sp
from sympy import symbols, solve, simplify

x, t = symbols('x t', real=True)
b = -10

# f(x) = x^3 - 10x
f = lambda x_val: x_val**3 - 10*x_val

# 검증: alpha = sqrt(10)
alpha_sq = 10
assert f(sp.sqrt(10)) == 0, 'f(sqrt(10)) should be 0'

# 검증: t=8에서 접촉점 확인
# 변 4: y = 2x - 2t와의 교점 방정식
h2 = x**3 - 12*x + 16  # t=8일 때
h2_prime = sp.diff(h2, x)
roots_h2_prime = solve(h2_prime, x)
assert any(sp.simplify(h2.subs(x, r)) == 0 for r in roots_h2_prime if r.is_real), 't=8에서 중근 존재'

# f(4) 계산
f_4 = f(4)
assert f_4 == 24, f'f(4) should be 24, got {f_4}'

# 최종 답
answer = alpha_sq * f_4
assert answer == 240, f'Final answer should be 240, got {answer}'

print('VERIFY_PASS')