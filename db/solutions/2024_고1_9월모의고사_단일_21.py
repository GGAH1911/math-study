import sympy as sp

x = sp.Symbol('x')
a, b, c = 2, 2, 5
f = (x - a)**2 + b
g = -sp.Rational(1, 2)*(x - c)**2 + 11

# roots of f = g
roots = sorted(sp.solve(f - g, x))
alpha, beta = roots[0], roots[1]
assert alpha == 1 and beta == 5, (alpha, beta)

def h(t):
    if alpha <= t <= beta:
        return f.subs(x, t)
    return g.subs(x, t)

# Verify k=2 yields exactly 3 intersection points with sum S
# left: g=2 on x<alpha; middle: f=2 on [alpha,beta]; right: g=2 on x>beta
left2 = [s for s in sp.solve(g - 2, x) if s < alpha]
mid2  = [s for s in sp.solve(f - 2, x) if alpha <= s <= beta]
right2= [s for s in sp.solve(g - 2, x) if s > beta]
pts2 = left2 + mid2 + right2
assert len(set(pts2)) == 3, pts2
S = sum(pts2)

# Verify k=3
left3 = [s for s in sp.solve(g - 3, x) if s < alpha]
mid3  = [s for s in sp.solve(f - 3, x) if alpha <= s <= beta]
right3= [s for s in sp.solve(g - 3, x) if s > beta]
pts3 = sorted(set(list(left3) + list(mid3) + list(right3) + [alpha, beta] if False else list(left3)+list(mid3)+list(right3)))
# include boundary alpha if g(alpha)=3 (it equals f(alpha))
all3 = sorted(set(list(left3)+list(mid3)+list(right3)))
assert len(all3) == 3, all3
T = sum(all3)

assert T - S == sp.Rational(a, 2), (T, S, T-S)

# Check that ONLY k=2 and k=3 produce exactly 3 intersections
import itertools
def count_intersections(k):
    L = [s for s in sp.solve(g - k, x) if s.is_real and s < alpha]
    M = [s for s in sp.solve(f - k, x) if s.is_real and alpha <= s <= beta]
    R = [s for s in sp.solve(g - k, x) if s.is_real and s > beta]
    return len(set(L + M + R))

for k_test in [-1, 0, 1, sp.Rational(3,2), 2, sp.Rational(5,2), 3, 4, 7, 11, 12]:
    n = count_intersections(k_test)
    if k_test in (2, 3):
        assert n == 3, (k_test, n)
    else:
        assert n != 3, (k_test, n)

# Final answer
val = h(alpha + beta)
assert val == sp.Rational(21, 2), val

print('VERIFY_PASS')
