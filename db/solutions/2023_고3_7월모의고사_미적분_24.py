import sympy as sp

x = sp.Symbol('x')
f = sp.ln(x**2 - x + 2)
f_prime = sp.diff(f, x)

# g(2) = 4, g'(2) = 12 from the limit condition
g2 = 4
g_prime2 = 12

# f'(g(2)) = f'(4)
f_prime_at_g2 = f_prime.subs(x, g2)

# h'(2) = f'(g(2)) * g'(2)
h_prime_2 = f_prime_at_g2 * g_prime2

# Verify the limit condition: lim (g(x)-4)/(x-2) = 12 means g(2)=4, g'(2)=12
# Check f'(4) = 7/14 = 1/2
assert f_prime_at_g2 == sp.Rational(1, 2), f'f_prime at 4 = {f_prime_at_g2}'
assert h_prime_2 == 6, f'h_prime_2 = {h_prime_2}'

print('VERIFY_PASS')