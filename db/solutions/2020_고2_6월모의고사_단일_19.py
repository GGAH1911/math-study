import sympy as sp
# A(-1,0),B(1,0) 원 위 P, ∠PAB=θ → P=(cos2θ,sin2θ). PB 위 PQ=3 점 Q. Q_x 최대일 때 sin²θ? (③=9/16)
# Q_x = cos2θ + 3·(1-cos2θ)/(2sinθ) = 1-2s²+3s  (s=sinθ)
CANDIDATE = sp.Rational(9, 16)
s = sp.symbols('s', positive=True)
Qx = 1 - 2*s**2 + 3*s
sv = sp.solve(sp.diff(Qx, s), s)[0]                          # 3/4
print('VERIFY_PASS' if sv**2 == CANDIDATE else 'VERIFY_FAIL')
