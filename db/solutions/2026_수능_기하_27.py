from sympy import *

h = sqrt(21)
r = Rational(5,2)

# Points
A = Matrix([Rational(-5,2), 0, 0])
B = Matrix([Rational(5,2), 0, 0])
C = Matrix([Rational(3,2), 2, h])
D = Matrix([Rational(-3,2), 2, h])
H = Matrix([Rational(-3,2), 2, 0])

# Check radii
assert simplify(A[0]**2 + A[1]**2 - r**2) == 0, 'A not on C1'
assert simplify(B[0]**2 + B[1]**2 - r**2) == 0, 'B not on C1'
assert simplify(C[0]**2 + C[1]**2 - r**2) == 0, 'C not on C2'
assert simplify(D[0]**2 + D[1]**2 - r**2) == 0, 'D not on C2'

# Check AB=5
assert simplify((B-A).norm() - 5) == 0, 'AB != 5'

# Check CD=3
assert simplify((D-C).norm() - 3) == 0, 'CD != 3'

# Check AD=BC
AD = simplify((D-A).norm())
BC = simplify((C-B).norm())
assert simplify(AD - BC) == 0, f'AD != BC: {AD} vs {BC}'

# Check H is foot of perp from D
assert H[0] == D[0] and H[1] == D[1] and H[2] == 0, 'H wrong'

# Area of triangle ABH
cross_ABH = (B-A).cross(H-A)
area_ABH = Rational(1,2) * simplify(cross_ABH.norm())

# Area of quadrilateral ABCD = triangle ABD + triangle BCD
cross1 = (B-A).cross(D-A)
area1 = Rational(1,2) * simplify(cross1.norm())
cross2 = (C-B).cross(D-B)
area2 = Rational(1,2) * simplify(cross2.norm())
area_ABCD = simplify(area1 + area2)

if simplify(area_ABCD - 4*area_ABH) == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: area_ABCD={area_ABCD}, 4*area_ABH={4*area_ABH}')
