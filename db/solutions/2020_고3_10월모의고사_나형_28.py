CANDIDATE = 160
import sympy as sp
x = sp.symbols('x', real=True)

def distinct_real_root_count(a):
    f = 2*x**3 - 3*(a+1)*x**2 + 6*a*x
    roots = sp.solve(sp.Eq(f, 0), x)
    reals = []
    for r in roots:
        rn = complex(sp.N(r))
        if abs(rn.imag) < 1e-9:
            reals.append(rn.real)
    distinct = []
    for r in reals:
        if not any(abs(r - d) < 1e-9 for d in distinct):
            distinct.append(r)
    return len(distinct)

# a_1..a_10: natural numbers giving exactly 3 distinct real roots
valid_a = []
a_val = 1
while len(valid_a) < 10:
    if distinct_real_root_count(a_val) == 3:
        valid_a.append(a_val)
    a_val += 1

total = sp.Integer(0)
for n, a in enumerate(valid_a, start=1):
    a_s = sp.Integer(a)
    f = 2*x**3 - 3*(a_s+1)*x**2 + 6*a_s*x
    crit = sp.solve(sp.diff(f, x), x)
    fpp = sp.diff(f, x, 2)
    bmax = None
    for c in crit:
        if fpp.subs(x, c) < 0:  # local maximum
            bmax = f.subs(x, c)
    total += (bmax - a_s)

total = sp.simplify(total)
print('VERIFY_PASS' if total == CANDIDATE else 'VERIFY_FAIL ' + str(total))