import sympy as sp
from sympy import symbols, integrate, diff, Rational, solve, simplify, S, sqrt

t = symbols('t', real=True)

def analyze(a_v, b_v):
    x_e = t * (t - 1) * (a_v*t + b_v)
    v_e = diff(x_e, t)
    crit = [r for r in solve(v_e, t) if r.is_real and r > 0 and r < 1]
    pts = sorted([S(0)] + crit + [S(1)])
    td = sum(abs(x_e.subs(t, pts[i+1]) - x_e.subs(t, pts[i])) for i in range(len(pts)-1))
    max_x = max([abs(x_e.subs(t, cp)) for cp in crit] + [S(0)])
    zeros = [r for r in solve(x_e, t) if r.is_real and r > 0 and r < 1]
    int_v = integrate(v_e, (t, 0, 1))
    return simplify(td), simplify(max_x), zeros, simplify(int_v)

# Case A: -b/a = 0 (Case A boundary). x = (27/4) t^2 (t-1). max|x|=1 at t=2/3.
td_A, mx_A, zs_A, iv_A = analyze(Rational(27, 4), 0)
# Case B: -b/a = 1/2. x = 6 sqrt(3) t(t-1)(t-1/2). max|x|=1/2, has zero at 1/2.
td_B, mx_B, zs_B, iv_B = analyze(6*sqrt(3), -3*sqrt(3))

# ㄱ : integral of v is 0 (since x(0)=x(1)=0)
g_ok = (iv_A == 0) and (iv_B == 0)
# total distance equals 2 in both constructed cases
td_ok = (simplify(td_A - 2) == 0) and (simplify(td_B - 2) == 0)
# ㄴ should be FALSE: max|x| never exceeds 1
n_false = bool(mx_A <= 1) and bool(mx_B <= 1) and (not bool(mx_A > 1)) and (not bool(mx_B > 1))
# ㄷ should be TRUE:
#   Case A: hypothesis |x|<1 fails (mx_A=1), implication vacuously true
#   Case B: hypothesis holds (mx_B=1/2<1) and zero at 1/2 in (0,1) exists
caseA_hyp = bool(mx_A < 1)
caseB_hyp = bool(mx_B < 1)
d_A = (not caseA_hyp) or (len(zs_A) > 0)
d_B = (not caseB_hyp) or any(simplify(z - Rational(1, 2)) == 0 for z in zs_B)
d_ok = d_A and d_B
# Also sanity-check structural facts of cases
structure = (mx_A == 1) and (len(zs_A) == 0) and (mx_B == Rational(1,2)) and (Rational(1,2) in zs_B)

if g_ok and td_ok and n_false and d_ok and structure:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
