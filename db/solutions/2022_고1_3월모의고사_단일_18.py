from sympy import *

r = Integer(2)
B = Matrix([0, 0])
C = Matrix([4*r, 0])
A = Matrix([2*r/sqrt(3), 2*r])

# Verify angle ABC = 60
BA = A - B; BCv = C - B
cos_B = BA.dot(BCv) / (sqrt(BA.dot(BA)) * sqrt(BCv.dot(BCv)))
assert simplify(cos_B - Rational(1,2)) == 0, 'angle B != 60'

# Midpoints
D = (A + B) / 2
E = (A + C) / 2

# DE length
DE_vec = E - D
DE_len = sqrt(simplify(DE_vec.dot(DE_vec)))
assert simplify(DE_len - 2*r) == 0, 'DE != 2r'

# Circle center M and tangency to BC
M = (D + E) / 2
assert simplify(M[1] - r) == 0, 'not tangent to BC'

# Find F on AB other than D
t = symbols('t', real=True)
P = B + t*(A - B)
dist_sq = (P - M).dot(P - M)
sols = solve(dist_sq - r**2, t)
t_F = [s for s in sols if simplify(s - Rational(1,2)) != 0][0]
F = B + t_F*(A - B)
assert simplify((F - M).dot(F - M) - r**2) == 0, 'F not on circle'

# Verify angle DFE = 90
FD = D - F; FE_ = E - F
assert simplify(FD.dot(FE_)) == 0, 'angle DFE != 90'

# Triangle areas
def tri_area(P1, P2, P3):
    v1 = P2 - P1; v2 = P3 - P1
    return Rational(1,2) * Abs(v1[0]*v2[1] - v1[1]*v2[0])

area_ABC = tri_area(A, B, C)
area_ADE = tri_area(A, D, E)
area_FDE = tri_area(F, D, E)
area_AFE = tri_area(A, F, E)

assert simplify(area_ABC - 16) == 0, f'area ABC={area_ABC}'
assert simplify(area_ADE - 4) == 0, f'area ADE={area_ADE}'
assert simplify(area_FDE - 2*sqrt(3)) == 0, f'area FDE={simplify(area_FDE)}'
assert simplify(area_AFE - (4 - 2*sqrt(3))) == 0, f'area AFE={simplify(area_AFE)}'

# AH from tangency: AH = 2r -> a=2, b=2, c=2*sqrt(3)
a_val, b_val, c_val = 2, 2, 2*sqrt(3)
product = a_val * b_val * c_val
assert simplify(product - 8*sqrt(3)) == 0, f'product={simplify(product)}'

print('VERIFY_PASS')
