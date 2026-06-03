import numpy as np

a2 = 24/5
b_sq = 3.0
a_val = np.sqrt(a2)
c = np.sqrt(a2 + b_sq)
F = np.array([c, 0.0])
Fp = np.array([-c, 0.0])

# P: Q1 위 쌍곡선 점이면서 PF ⊥ PF' (즉 |OP|=c)
Px_sq = a2 * (b_sq + c**2) / (a2 + b_sq)
Px = np.sqrt(Px_sq)
Py_sq = c**2 - Px_sq
Py = np.sqrt(Py_sq)
P = np.array([Px, Py])

# 1) 쌍곡선 위 확인
hyp_res = Px**2/a2 - Py**2/b_sq - 1.0
# 2) PF ⊥ PF' 확인
perp_res = float((P-F) @ (P-Fp))

# Q: PF' 선분 위 |PQ| = a/3
v = Fp - P
r2 = np.linalg.norm(v)
Q = P + (a_val/3.0) * v / r2
pq = np.linalg.norm(Q - P)

# A: 직선 QF와 y축의 교점
denom = c - Q[0]
t = c / denom
A = F + t * (Q - F)
ax_res = A[0]

# AR, AS: A에서 직선 PF, PF'까지의 수선의 길이
def pdist(A, P1, P2):
    d = P2 - P1
    n = np.array([-d[1], d[0]])
    return abs(float((A-P1) @ n)) / float(np.linalg.norm(d))

AR = pdist(A, P, F)
AS = pdist(A, P, Fp)

tol = 1e-8
ok = (abs(hyp_res) < tol and abs(perp_res) < tol and
      abs(pq - a_val/3.0) < tol and abs(ax_res) < tol and
      abs(AR - AS) < tol)
print('VERIFY_PASS' if ok else 'VERIFY_FAIL')
