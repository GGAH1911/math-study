import sympy as sp

x = sp.Symbol('x')
f = x**3 + 4*x**2 - 28*x + 35
f_prime = sp.diff(f, x)

# 점 (2, 3)이 곡선 위에 있는지
assert f.subs(x, 2) == 3, "f(2) must equal 3"

# 점 (2, 3)에서의 접선이 (1, 3)을 지나는지
f_2 = f.subs(x, 2)
f_prime_2 = f_prime.subs(x, 2)
assert f_prime_2 == 0, "f'(2) must equal 0"
tangent_at_2 = f_2 + f_prime_2 * (1 - 2)
assert tangent_at_2 == 3, "Tangent at (2,3) must pass through (1,3)"

# 점 (-2, f(-2))에서의 접선이 (1, 3)을 지나는지
f_minus2 = f.subs(x, -2)
f_prime_minus2 = f_prime.subs(x, -2)
tangent_at_minus2 = f_minus2 + f_prime_minus2 * (1 - (-2))
assert tangent_at_minus2 == 3, "Tangent at (-2, f(-2)) must pass through (1,3)"

# 답 검증
answer_value = f.subs(x, 0)
assert answer_value == 35, f"f(0) must equal 35, got {answer_value}"

print('VERIFY_PASS')