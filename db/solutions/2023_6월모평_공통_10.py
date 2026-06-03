import sympy as sp

# Given values
AB = 3
BC = 2
cos_A = sp.Rational(7, 8)

# Find AC via law of cosines: BC^2 = AB^2 + AC^2 - 2*AB*AC*cos_A
b = sp.Symbol('b', positive=True)
eq = sp.Eq(BC**2, AB**2 + b**2 - 2*AB*b*cos_A)
sols = sp.solve(eq, b)
AC = max(s for s in sols if s > 3)  # AC > 3
assert AC == 4, f'AC={AC}'

# M is midpoint of AC
AM = MC = AC / 2  # = 2

# Median BM
BM_sq = (2*AB**2 + 2*BC**2 - AC**2) / 4
BM = sp.sqrt(BM_sq)
assert BM == sp.sqrt(10)/2

# Intersecting chords theorem: AM * MC = BM * MD
MD = AM * MC / BM
MD_simplified = sp.simplify(MD)

expected = 4*sp.sqrt(10)/5
if sp.simplify(MD_simplified - expected) == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: MD={MD_simplified}, expected={expected}')
