import sympy as sp

k = sp.Symbol('k', positive=True)

# Points
def P(kv): return (sp.Integer(0), 4*kv)
def Q(kv): return (4*kv, sp.Integer(4))
def R(kv): return (sp.Integer(4), 4*(1-kv))

# Circle center (2,2), r^2 = 8 - 16k + 16k^2
cx, cy = sp.Integer(2), sp.Integer(2)
r2_expr = 8 - 16*k + 16*k**2

# Verify center is equidistant from P, Q, R
def dist2(pt, kv):
    return (pt[0] - cx.subs(k, kv) if hasattr(cx,'subs') else pt[0] - 2)**2 + \
           (pt[1] - cy.subs(k, cy) if hasattr(cy,'subs') else pt[1] - 2)**2

for pt_fn in [P, Q, R]:
    d2 = sp.expand((pt_fn(k)[0]-2)**2 + (pt_fn(k)[1]-2)**2)
    assert sp.simplify(d2 - r2_expr) == 0, f'Center check failed for {pt_fn}'

# ㄱ: m=n => k=1/2, P=(0,2)
k1 = sp.Rational(1,2)
P1 = P(k1)
assert P1 == (0, 2), f'ㄱ failed: P={P1}'

# ㄴ: (4k, 0) is on the circle for all k
point_L = (4*k, sp.Integer(0))
dist2_L = sp.expand((point_L[0]-2)**2 + (point_L[1]-2)**2)
diff_L = sp.simplify(dist2_L - r2_expr)
assert diff_L == 0, f'ㄴ failed: diff={diff_L}'

# ㄷ: distance between x-intercepts = 3 => PQ = 5*sqrt(2)/2
# x-intercepts: x1=4k, x2=4-4k, dist=4|2k-1|=3 => k=7/8 or 1/8
for kv in [sp.Rational(7,8), sp.Rational(1,8)]:
    Ppt = P(kv); Qpt = Q(kv)
    PQ = sp.sqrt((Qpt[0]-Ppt[0])**2 + (Qpt[1]-Ppt[1])**2)
    target = 5*sp.sqrt(2)/2
    assert sp.simplify(PQ - target) == 0, f'ㄷ failed at k={kv}: PQ={PQ}'

print('VERIFY_PASS')
