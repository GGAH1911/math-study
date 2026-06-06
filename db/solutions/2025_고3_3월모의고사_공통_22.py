import sympy as sp

x = sp.Symbol('x')
f = -x**3 + x**2 + 4

# 조건 검증
f_at_0 = f.subs(x, 0)
f_prime = sp.diff(f, x)
f_prime_at_0 = f_prime.subs(x, 0)
f_at_2 = f.subs(x, 2)
f_prime_at_2 = f_prime.subs(x, 2)

# g(x) 미분가능성 검증
g_left_0 = -f_prime_at_0
g_right_0 = f_prime_at_0

g_left_2 = f_prime_at_2 + 8
g_right_2 = -f_prime_at_2 - 8

# 결과
assert f_at_0 == 4, f"f(0) = {f_at_0}, expected 4"
assert f_prime_at_0 == 0, f"f'(0) = {f_prime_at_0}, expected 0"
assert f_at_2 == 0, f"f(2) = {f_at_2}, expected 0"
assert f_prime_at_2 == -8, f"f'(2) = {f_prime_at_2}, expected -8"
assert g_left_0 == g_right_0, f"g'(0-) = {g_left_0}, g'(0+) = {g_right_0}"
assert g_left_2 == g_right_2, f"g'(2-) = {g_left_2}, g'(2+) = {g_right_2}"

f_at_minus5 = f.subs(x, -5)
assert f_at_minus5 == 154, f"f(-5) = {f_at_minus5}"

print('VERIFY_PASS')