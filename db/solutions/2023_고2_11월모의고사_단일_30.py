import sympy as sp
from sympy import symbols, integrate, solve

x = symbols('x')
# f(x) = 2x(x-2)(x-4)
f = 2*x*(x-2)*(x-4)

# 검증 조건들
assert f.subs(x, 0) == 0, "f(0) should be 0"
assert f.subs(x, 2) == 0, "f(2) should be 0"

f_prime = sp.diff(f, x)
assert f_prime.subs(x, 2) < 0, "f'(2) should be negative"

# F(x) = ∫_0^x f(t)dt
F = integrate(f, (x, 0, x))
assert F.subs(x, 2) == 8, "F(2) should be 8"
assert F.subs(x, 4) == 0, "F(4) should be 0"

# g(x) = 4 방정식 확인
# x < 2: F(x) - 4 = 4 ⟹ F(x) = 8
# x ≥ 2: -F(x) + 4 = 4 ⟹ F(x) = 0
roots_left = solve(F - 8, x)
roots_right = solve(F, x)

# 정확히 2개의 실근 확인
valid_roots_left = [r for r in roots_left if r.is_real and r < 2]
valid_roots_right = [r for r in roots_right if r.is_real and r >= 2]
total_roots = len(valid_roots_left) + len(valid_roots_right)

assert total_roots == 2, f"Should have exactly 2 roots, got {total_roots}"

# 최종 답
result = f.subs(x, 5)
assert result == 30, f"f(5) should be 30, got {result}"

print('VERIFY_PASS')