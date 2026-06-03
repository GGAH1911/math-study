import numpy as np

# Claim: |FF'| = 4*sqrt(5)
FF_claim = 4 * np.sqrt(5)
c = FF_claim / 2
b_sq = 16
a_sq = c**2 - b_sq  # from c^2 = a^2 + b^2 for hyperbola
if a_sq <= 0:
    print('VERIFY_FAIL'); raise SystemExit
a = np.sqrt(a_sq)
F = np.array([c, 0.0])
Fp = np.array([-c, 0.0])

# Search for P on right branch (Q1) such that |PF| = |QF|; |PQ|=8 follows from focal property
def compute_Q(P):
    dx, dy = P[0] - Fp[0], P[1] - Fp[1]
    A_ = dx**2/a_sq - dy**2/b_sq
    B_ = 2*Fp[0]*dx/a_sq
    C_ = Fp[0]**2/a_sq - 1
    disc = B_**2 - 4*A_*C_
    if disc < 0: return None
    s1 = (-B_ + np.sqrt(disc))/(2*A_)
    s2 = (-B_ - np.sqrt(disc))/(2*A_)
    sQ = s2 if abs(s1 - 1) < abs(s2 - 1) else s1
    return Fp + sQ * np.array([dx, dy])

def residual(t):
    P = np.array([a*np.cosh(t), np.sqrt(b_sq)*np.sinh(t)])
    Q = compute_Q(P)
    if Q is None: return None, None, None
    PF = np.linalg.norm(P - F); QF = np.linalg.norm(Q - F)
    return PF - QF, P, Q

ts = np.linspace(0.05, 4.0, 4000)
prev_r, prev_t = None, None
found = None
for t in ts:
    r, P, Q = residual(t)
    if r is None:
        prev_r = None; continue
    if prev_r is not None and r * prev_r < 0:
        lo, hi = prev_t, t; rlo = prev_r
        for _ in range(100):
            mid = (lo + hi)/2
            rm, Pm, Qm = residual(mid)
            if rm is None: break
            if rm * rlo > 0: lo, rlo = mid, rm
            else: hi = mid
        tt = (lo + hi)/2
        rr, Pf, Qf = residual(tt)
        found = (tt, Pf, Qf); break
    prev_r, prev_t = r, t

if found is None:
    print('VERIFY_FAIL'); raise SystemExit
_, P, Q = found

on_hyp_P = abs(P[0]**2/a_sq - P[1]**2/b_sq - 1) < 1e-8
on_hyp_Q = abs(Q[0]**2/a_sq - Q[1]**2/b_sq - 1) < 1e-8
PF_v = np.linalg.norm(P - F)
QF_v = np.linalg.norm(Q - F)
PQ_v = np.linalg.norm(P - Q)
FF_v = np.linalg.norm(F - Fp)
P_in_Q1 = P[0] > 0 and P[1] > 0
# Check line F'-Q-P collinear and Q between F' and P
vec_FpP = P - Fp; vec_FpQ = Q - Fp
cross = abs(vec_FpP[0]*vec_FpQ[1] - vec_FpP[1]*vec_FpQ[0])
dot = vec_FpP.dot(vec_FpQ)
collinear = cross < 1e-6
Q_between = 0 < dot < vec_FpP.dot(vec_FpP)

ok = (on_hyp_P and on_hyp_Q and abs(PF_v - QF_v) < 1e-5
      and abs(PQ_v - 8) < 1e-5 and abs(FF_v - 4*np.sqrt(5)) < 1e-8
      and P_in_Q1 and collinear and Q_between)
print('VERIFY_PASS' if ok else 'VERIFY_FAIL')
