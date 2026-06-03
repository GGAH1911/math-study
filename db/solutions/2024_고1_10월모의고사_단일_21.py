import numpy as np

C1c = np.array([2.,6.]); r1 = 1.
C2c = np.array([6.,4.]); r2 = 3.

def min_expr(X, cc, rad, n=5000):
    best = np.inf
    for r in np.linspace(-60, 60, n):
        R  = np.array([0.,  r])
        Rp = np.array([0., -r])
        # closest P on circle to Rp: |distance(Rp,cc) - rad|
        d = abs(np.linalg.norm(Rp - cc) - rad)
        val = np.linalg.norm(X - R) + d
        if val < best:
            best = val
    return best

# ㄱ : AR = A'R' for every r on y-axis
A  = np.array([4., 2.])
Ap = np.array([4.,-2.])
ok_g = True
for r in np.linspace(-20, 20, 500):
    R  = np.array([0.,  r])
    Rp = np.array([0., -r])
    if abs(np.linalg.norm(A-R) - np.linalg.norm(Ap-Rp)) > 1e-10:
        ok_g = False; break

# ㄴ : min |AR| + |PR'| should be 9
m_n  = min_expr(A, C1c, r1)
ok_n = abs(m_n - 9.0) < 1e-3

# ㄷ : with a = 1/2, B = (1/2, 4), the equality holds and OB = sqrt(65)/2
a  = 0.5
B  = np.array([a, 6*a + 1])
m1 = min_expr(B, C1c, r1)
m2 = min_expr(B, C2c, r2)
ok_d_cond = abs(m1 - (m2 + 2)) < 1e-3
OB = float(np.linalg.norm(B))
ok_d_OB = abs(OB - np.sqrt(65)/2) < 1e-12
ok_d = ok_d_cond and ok_d_OB

# also confirm that no other positive a satisfies the equation
import sympy as sp
x = sp.symbols('a', positive=True)
eq = sp.Eq(sp.sqrt((x+2)**2 + (6*x+7)**2) - 1, sp.sqrt((x+6)**2 + (6*x+5)**2) - 1)
sols = sp.solve(eq, x)
ok_unique = (len(sols) == 1 and sp.simplify(sols[0] - sp.Rational(1,2)) == 0)

chosen = 5
print('VERIFY_PASS' if (chosen == 5 and ok_g and ok_n and ok_d and ok_unique) else 'VERIFY_FAIL')
