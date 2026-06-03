import sympy as sp
x = sp.symbols('x')
valid = []
for n_val in range(1, 21):
    poly = sp.Poly(4*x**4 - 4*(n_val+2)*x**2 + (n_val-2)**2, x)
    roots_dict = sp.roots(poly)
    int_roots = [r for r in roots_dict.keys() if r.is_integer]
    if len(int_roots) == 4:
        valid.append(n_val)
if sorted(valid) != [8, 18]:
    print('VERIFY_FAIL')
else:
    a, b = 8, 18
    # f(n) determined from discriminant: (n+2)^2 - (n-2)^2 = 8n
    n_sym = sp.symbols('n')
    disc = sp.expand((n_sym+2)**2 - (n_sym-2)**2)
    f = sp.lambdify(n_sym, disc)
    result = f(b - a)
    print('VERIFY_PASS' if result == 80 else 'VERIFY_FAIL')
