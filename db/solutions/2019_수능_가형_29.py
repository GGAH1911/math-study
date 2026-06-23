from sympy import symbols, Piecewise, simplify, integrate
import numpy as np
from scipy.spatial import ConvexHull

CANDIDATE = 53

# 육각형 꼭짓점
vertices = np.array([
    [0.5, 0],
    [0.75, 0],
    [0.75, 0.25],
    [0.25, 0.75],
    [0, 0.75],
    [0, 0.5]
])

# Shoelace 공식
def shoelace_area(vertices):
    n = len(vertices)
    area = 0
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i+1) % n]
        area += x1*y2 - x2*y1
    return abs(area) / 2

area_alpha_beta = shoelace_area(vertices)
triangle_area = 9
jac_det = 18  # |AB × AC| = 2 * 9 = 18
area_X = area_alpha_beta * jac_det

# 기약분수로 표현
from fractions import Fraction
frac = Fraction(area_X).limit_denominator()
q, p = frac.numerator, frac.denominator
answer = p + q

if answer == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")