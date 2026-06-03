import math

def solve_bisect(fn, a, b, tol=1e-10):
    fa, fb = fn(a), fn(b)
    if fa*fb > 0:
        return None
    for _ in range(300):
        c = 0.5*(a+b)
        fc = fn(c)
        if abs(fc) < tol or (b-a) < tol:
            return c
        if fa*fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    return 0.5*(a+b)

def count_roots(t):
    g = lambda x: abs(2**(-x+3) - 2)
    h = lambda x: -x*x + t*x - 4
    if t*t - 16 <= 0:
        return -1
    r1 = (t - math.sqrt(t*t - 16))/2
    r2 = (t + math.sqrt(t*t - 16))/2
    diff = lambda x: g(x) - h(x)
    alpha = solve_bisect(diff, r1+1e-9, 2-1e-9)
    beta = solve_bisect(diff, 2+1e-9, r2-1e-9)
    if alpha is None or beta is None:
        return -1
    def f(x):
        return g(x) if (x < alpha or x > beta) else h(x)
    c = f(t/2)
    roots = []
    r = solve_bisect(lambda x: g(x)-c, -50.0, alpha-1e-9)
    if r is not None: roots.append(r)
    disc = t*t - 4*(4+c)
    if disc >= -1e-12:
        d = math.sqrt(max(disc, 0.0))
        for s in (-1, 1):
            x = (t + s*d)/2
            if alpha-1e-9 <= x <= beta+1e-9:
                roots.append(x)
    r = solve_bisect(lambda x: g(x)-c, beta+1e-9, 50.0)
    if r is not None: roots.append(r)
    unique = []
    for r in roots:
        if not any(abs(r-u) < 1e-5 for u in unique):
            unique.append(r)
    return len(unique)

t_ans = 2*math.sqrt(6)
n_at = count_roots(t_ans)
n_below = count_roots(t_ans - 0.01)
n_above = count_roots(t_ans + 0.01)

if n_at == 2 and n_below > 2 and n_above == 2:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: at={n_at}, below={n_below}, above={n_above}')
