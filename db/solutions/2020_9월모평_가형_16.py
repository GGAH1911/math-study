from sympy import *
from sympy.geometry import Point3D, Plane, Line3D, Segment3D
import math

A = Point3D(3, 0, 0)
B = Point3D(0, 3, 0)
C = Point3D(0, 2, 1)
D = Point3D(0, Rational(-5,2), -2)

E = Point3D((C.x + 2*D.x)/3, (C.y + 2*D.y)/3, (C.z + 2*D.z)/3)
print(f'E = {E}')

vec_AE = (E.x - A.x, E.y - A.y, E.z - A.z)
print(f'vec_AE = {vec_AE}')

length_AE = sqrt(vec_AE[0]**2 + vec_AE[1]**2 + vec_AE[2]**2)
print(f'|AE| = {length_AE}')

plane = Plane(A, B, C)
print(f'Plane ABC: {plane}')

dist_E_to_plane = plane.distance(E)
print(f'Distance from E to plane: {dist_E_to_plane}')

projection_length = sqrt(length_AE**2 - dist_E_to_plane**2)
print(f'Projection length: {projection_length}')
print(f'Simplified: {simplify(projection_length)}')

answer_value = Rational(2,3) * sqrt(6)
if simplify(projection_length - answer_value) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')