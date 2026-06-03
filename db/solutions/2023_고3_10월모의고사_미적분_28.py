import sympy as sp

x, a, b = sp.symbols('x a b', real=True)
f = sp.sin(x) * sp.cos(x) * sp.exp(a * sp.sin(x) + b * sp.cos(x))

candidates = []
for v in [sp.Rational(1, 2), sp.Integer(-1)]:
    candidates.append((v, sp.Integer(0)))  # b=0
    candidates.append((sp.Integer(0), v))  # a=0

valid_pairs = []
for av, bv in candidates:
    if av == bv:
        continue
    if av * bv != 0:
        continue
    f_sub = f.subs([(a, av), (b, bv)])
    LHS = sp.integrate(f_sub, (x, 0, sp.pi / 2))
    RHS = sp.Rational(1) / (av**2 + bv**2) - 2 * sp.exp(av + bv)
    if sp.simplify(LHS - RHS) == 0:
        valid_pairs.append((av, bv))

diffs = [av - bv for av, bv in valid_pairs]
min_diff = min(diffs)

expected = sp.Integer(-1)
if min_diff == expected and len(valid_pairs) == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
