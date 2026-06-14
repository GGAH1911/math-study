import sympy as sp

x = sp.Symbol('x', real=True)

def g(t):
    return t**2 - 6*t + 10

def distinct_real_roots(expr):
    # exact number of DISTINCT real roots of a polynomial in x
    p = sp.Poly(sp.expand(expr), x)
    return len(p.sqf_part().real_roots())

# ===== Part A: derive local-max value M and local-min value L from the three conditions =====
# g(t) = (t-3)^2 + 1 -> global min 1 at t=3.  f is a cubic (surjective) -> min of g(f) is m = 1.
m = 1
t = sp.Symbol('t')
assert sp.expand(g(t) - ((t - 3)**2 + 1)) == 0

# distinct real solutions of f(x)=c for a cubic with local-max value M, local-min value L (M>L):
def level_roots(c, M, L):
    if c > M or c < L:
        return 1
    if c == M or c == L:
        return 2
    return 3

# (ga) f=0  -> 3 distinct roots            => level_roots(0,M,L)==3   (forces L<0<M)
# (na) g(f)=m=1 <=> f=3 -> 2 distinct       => level_roots(3,M,L)==2
# (da) g(f)=17 <=> f=7 or f=-1 -> total 3   => level_roots(7,M,L)+level_roots(-1,M,L)==3
sols = []
for Mn in range(-12, 13):
    for Ln in range(-12, 13):
        M, L = sp.Integer(Mn), sp.Integer(Ln)
        if M <= L:
            continue
        if (level_roots(0, M, L) == 3 and
            level_roots(3, M, L) == 2 and
            level_roots(7, M, L) + level_roots(-1, M, L) == 3):
            sols.append((M, L))
assert sols == [(sp.Integer(3), sp.Integer(-1))], sols
M, L = sols[0]
answer_sum = M + L

# ===== Part B: confirm with an explicit cubic realizing (M,L)=(3,-1) via exact root counts =====
f = x**3 - 3*x**2 + 3                 # f'(x)=3x(x-2): f(0)=3 (max), f(2)=-1 (min)
crit = sp.solve(sp.diff(f, x), x)     # [0, 2]
ext = sorted(int(f.subs(x, c)) for c in crit)
assert ext[0] == int(L) and ext[-1] == int(M)
assert ext[0] + ext[-1] == answer_sum

gf = g(f)                             # g(f(x))
assert distinct_real_roots(f) == 3                         # (ga)
assert sp.expand(gf - m) == sp.expand((f - 3)**2)          # (na) g(f)-1 is a perfect square -> min 1
assert distinct_real_roots(f - 3) >= 1                     #      value 3 attained -> min exactly m=1
assert distinct_real_roots(gf - m) == 2                    # (na) g(f)=m has 2 distinct roots
assert distinct_real_roots(gf - 17) == 3                   # (da) g(f)=17 has 3 distinct roots

print('VERIFY_PASS' if answer_sum == 2 else 'VERIFY_FAIL')
