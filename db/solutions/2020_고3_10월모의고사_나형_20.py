from sympy import symbols, integrate, diff, solve, simplify

x, c = symbols('x c', real=True)

# f(x) = 4x^3 - 18x^2 + c
f = 4*x**3 - 18*x**2 + c
f_prime = diff(f, x)

# g(x) = integral from 0 to x of f(t)dt - x*f(x)
f_integral = integrate(f, (x, 0, x))
g = f_integral - x*f
g_prime = diff(g, x)

# Verify g'(x) = -x*f'(x)
verify_gprime = simplify(g_prime + x*f_prime)

# Calculate integral from 0 to 1 of g'(x)dx = g(1) - g(0)
g_at_0 = g.subs(x, 0)
g_at_1 = g.subs(x, 1)
result = g_at_1 - g_at_0
result = simplify(result)

# Verify by direct integration
direct_integral = integrate(g_prime, (x, 0, 1))
direct_integral = simplify(direct_integral)

if result == 9 and direct_integral == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')