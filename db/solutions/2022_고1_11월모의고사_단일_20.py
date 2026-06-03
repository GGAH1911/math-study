from sympy import sqrt, Rational, simplify, symbols, Matrix

k = symbols('k', positive=True)

# Circle C: center (k/2, -k/2), radius k*sqrt(2)/2
cx, cy = k/2, -k/2
r = k * sqrt(2) / 2

# Verify passes through O(0,0)
assert simplify(cx**2 + cy**2 - r**2) == 0, 'VERIFY_FAIL: not through O'

# Verify passes through A(k,0)
assert simplify((k-cx)**2 + cy**2 - r**2) == 0, 'VERIFY_FAIL: not through A'

# Verify tangent to AB at A: CA ⊥ AB direction (-1,1)
CA = Matrix([k-cx, 0-cy])  # = (k/2, k/2)
AB_dir = Matrix([-1, 1])
assert simplify(CA.dot(AB_dir)) == 0, 'VERIFY_FAIL: not tangent at A'

# Verify angle OAC = 45 degrees
AO = Matrix([0-k, 0-0])  # = (-k, 0)
AC = Matrix([cx-k, cy-0])  # = (-k/2, -k/2)
cos_OAC = AO.dot(AC) / (AO.norm() * AC.norm())
assert simplify(cos_OAC - sqrt(2)/2) == 0, 'VERIFY_FAIL: angle OAC != 45'

# Maximum y on circle (topmost point, theta=90 deg)
P_y_max = cy + r  # = -k/2 + k*sqrt(2)/2 = k*(sqrt(2)-1)/2
assert simplify(P_y_max - k*(sqrt(2)-1)/2) == 0, 'VERIFY_FAIL: M(k) wrong'

# Verify angle PCO = 45 at P=(cx, cy+r)
CP = Matrix([0, r])  # = (0, k*sqrt(2)/2)
CO = Matrix([0-cx, 0-cy])  # = (-k/2, k/2)
cos_PCO = CP.dot(CO) / (CP.norm() * CO.norm())
assert simplify(cos_PCO - sqrt(2)/2) == 0, 'VERIFY_FAIL: angle PCO != 45'

# (ga): f(k) = -k/2
# (na): g(k) = k*sqrt(2)/2
# (da): p = (sqrt(2)-1)/2
def f(x): return -x/2
def g(x): return x * sqrt(2)/2

p = (sqrt(2)-1)/2
result = simplify(f(p) + g(Rational(1,2)))

if simplify(result - Rational(1,4)) == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: result={result}')
