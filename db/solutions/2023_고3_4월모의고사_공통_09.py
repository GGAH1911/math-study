from sympy import symbols, integrate, limit, diff, simplify

x, t = symbols('x t')
C = 1
f = x**3 - 2*x**2 + x + C
f_prime = 3*x**2 - 4*x + 1

# 검증 1: f'(x) = 3x^2 - 4x + 1
assert simplify(diff(f, x) - f_prime) == 0

# 검증 2: 극한 조건
f_t = t**3 - 2*t**2 + t + 1
integral = integrate(f_t, (t, 0, x))
limit_val = limit(integral/x, x, 0)
assert limit_val == 1

# 검증 3: f(2) = 3
result = f.subs(x, 2)
assert result == 3

print('VERIFY_PASS')