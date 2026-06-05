import sympy as sp
x = sp.Symbol('x')
a = -3
f = x**2 * (x + a)
f_prime = sp.diff(f, x)

# Check conditions
print('f(0) =', f.subs(x, 0))  # Should be 0
print('f\'(0) =', f_prime.subs(x, 0))  # Should be 0

# Check condition (나): f(x) = 0 has positive root
roots_f = sp.solve(f, x)
positive_roots = [r for r in roots_f if r > 0]
print('Positive roots of f(x)=0:', positive_roots)  # Should have x=3

# Check condition (다): |f(x)| = 4 has 3 distinct real roots
eq1 = f - 4
eq2 = f + 4
roots_eq1 = sp.solve(eq1, x)
roots_eq2 = sp.solve(eq2, x)
print('Roots of f(x)=4:', [float(r.evalf()) if r.is_real else r for r in roots_eq1])
print('Roots of f(x)=-4:', [float(r.evalf()) if r.is_real else r for r in roots_eq2])
real_roots_all = [r for r in roots_eq1 if r.is_real] + [r for r in roots_eq2 if r.is_real]
print('Total distinct real roots of |f(x)|=4:', len(set(real_roots_all)))

# Verify g(3)
f_3 = f.subs(x, 3)
f_prime_3 = f_prime.subs(x, 3)
g_3 = f_3 + abs(f_prime_3)
print('\nf(3) =', f_3)
print('f\'(3) =', f_prime_3)
print('g(3) =', g_3)

if g_3 == 9:
    print('\nVERIFY_PASS')
else:
    print('\nVERIFY_FAIL')