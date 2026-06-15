from sympy import symbols, solve, diff, simplify

# 최솟값이 0인 경우
a = -3/2

# f(x) = x^3 + ax^2 + 1/2
def f(x_val):
    return x_val**3 + a*x_val**2 + 1/2

def f_prime(x_val):
    return 3*x_val**2 + 2*a*x_val

# 검증: f(0) = 1/2
assert abs(f(0) - 0.5) < 1e-9, f"f(0) = {f(0)}, expected 0.5"

# 검증: f'(0) = 0
assert abs(f_prime(0)) < 1e-9, f"f'(0) = {f_prime(0)}, expected 0"

# 검증: 극값 위치 x = -2a/3 = 1
extreme_x = -2*a/3
assert abs(extreme_x - 1) < 1e-9, f"extreme point x = {extreme_x}, expected 1"

# 검증: 최솟값이 0
min_val = f(1)
assert abs(min_val) < 1e-9, f"f(1) = {min_val}, expected 0"

# ㄱ 검증: g(0) + g'(0) = 1/2
g_0 = f(0)
g_prime_0 = f_prime(0)
assert abs(g_0 + g_prime_0 - 0.5) < 1e-9, f"g(0)+g'(0) = {g_0 + g_prime_0}, expected 0.5"

# ㄴ 검증: g(1) < 3/2
g_1 = f(1)
assert g_1 < 1.5, f"g(1) = {g_1}, should be < 1.5"

# ㄷ 검증: g(2) = 5/2
g_2 = f(2)
assert abs(g_2 - 2.5) < 1e-9, f"g(2) = {g_2}, expected 2.5"

print('VERIFY_PASS')