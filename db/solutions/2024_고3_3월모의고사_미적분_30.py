from sympy import symbols, expand, diff

x = symbols('x')
f = (x - 5) * (x - 8) * (x - 9)
m = 6
answer = 84

# Verify f(m) = m
assert f.subs(x, m) == m, f"f({m}) should equal {m}"

# Verify f'(m) = 1
f_prime = diff(f, x)
assert f_prime.subs(x, m) == 1, "f'(m) should equal 1"

# Verify f'(m+1) <= 0
assert f_prime.subs(x, m+1) <= 0, "f'(m+1) should be <= 0"

# Verify g(12) = f(12) = 84
g_12 = f.subs(x, 12)
assert g_12 == answer, f"g(12) should be {answer}, got {g_12}"

print('VERIFY_PASS')