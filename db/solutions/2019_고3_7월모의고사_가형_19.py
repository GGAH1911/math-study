from sympy import sqrt, simplify, Matrix
a = sqrt(6) + sqrt(2)
s = sqrt(6) - sqrt(2)
t = 2*sqrt(2)
h = sqrt(15)

# Verify projections are equilateral with side 4
dist_PH = sqrt(a**2 + (a-t)**2)
dist_HQ = sqrt(s**2 + a**2)
dist_QP = sqrt((a-s)**2 + t**2)
assert simplify(dist_PH - 4) == 0
assert simplify(dist_HQ - 4) == 0
assert simplify(dist_QP - 4) == 0

# Area of triangle EQH
area_EQH = s * a / 2
assert simplify(area_EQH) == 2

# Normal vectors
PH = Matrix([-a, a-t, h])
PQ = Matrix([s-a, -t, h])
n = PH.cross(PQ)
magn = sqrt(n.dot(n))
cos_theta = abs(n[2]) / magn
cos_theta = simplify(cos_theta)
assert simplify(cos_theta - 2/3) == 0

# Projection area
proj_area = simplify(2 * cos_theta)
assert simplify(proj_area - 4/3) == 0
print('VERIFY_PASS')