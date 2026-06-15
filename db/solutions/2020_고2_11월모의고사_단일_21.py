import sympy as sp
import numpy as np

p = sp.Symbol('p', positive=True, real=True)

# Conditions check
# From |PQ|² = |PR|², we get t = 1-2p, s = p

# ㄱ Check: 3p + 2(1-2p) = 2?
G1 = 3*p + 2*(1-2*p) - 2
G1_simplified = sp.simplify(G1)
# Result: -p, which is 0 only if p=0, violating P≠A

# ㄴ Check: |QR| = √3 * p?
# |QR|² = (3p/2)² + (-p√3/2)² = 3p²
QR_squared = sp.Rational(9,4)*p**2 + sp.Rational(3,4)*3*p**2
QR = sp.sqrt(QR_squared)
N1 = QR - sp.sqrt(3)*p
N1_simplified = sp.simplify(N1)
# Result: 0 (True)

# ㄷ Check: When area_circumcircle_PBQ = 2*area_circumcircle_CRQ, p = (√21-3)/6?
# R_PBQ² = (1-3p+3p²)/3
# R_CRQ² = p²
# Condition: (1-3p+3p²)/3 = 2p²
eq = (1 - 3*p + 3*p**2)/3 - 2*p**2
eq_simplified = sp.simplify(eq)
# This gives: (1 - 3p - 3p²)/3 = 0 → 3p² + 3p - 1 = 0

quadratic = 3*p**2 + 3*p - 1
roots = sp.solve(quadratic, p)
positive_root = [r for r in roots if r > 0][0]

expected = (sp.sqrt(21) - 3) / 6
verify_root = sp.simplify(positive_root - expected)

if verify_root == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')