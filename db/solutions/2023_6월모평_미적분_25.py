from sympy import symbols, Rational, solve, diff

x = symbols('x')
f = x**3 + 2*x + 3
f_prime = diff(f, x)

# g(3): f(a) = 3
a = symbols('a')
sols = solve(f.subs(x, a) - 3, a)
real_sols = [s for s in sols if s.is_real]
g_3 = real_sols[0]  # should be 0

# f'(g(3))
f_prime_at_g3 = f_prime.subs(x, g_3)

# g'(3) = 1 / f'(g(3))
g_prime_3 = Rational(1, 1) / f_prime_at_g3

if g_prime_3 == Rational(1, 2):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
