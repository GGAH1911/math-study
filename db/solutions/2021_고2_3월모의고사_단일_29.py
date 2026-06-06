import numpy as np
from scipy.optimize import fsolve

a = np.sqrt(2)

# 원 위의 3개 점
P1 = np.array([np.sqrt(2), 2*np.sqrt(2)])
P2 = np.array([np.sqrt(2)-4, -2*np.sqrt(2)])
P3 = np.array([np.sqrt(2)+4, -2*np.sqrt(2)])

# 원의 방정식 검증
def circle_eq(x, y):
    return (x - a)**2 + (y + a)**2 - 9*a**2

assert abs(circle_eq(P1[0], P1[1])) < 1e-10, f'P1 not on circle: {circle_eq(P1[0], P1[1])}'
assert abs(circle_eq(P2[0], P2[1])) < 1e-10, f'P2 not on circle: {circle_eq(P2[0], P2[1])}'
assert abs(circle_eq(P3[0], P3[1])) < 1e-10, f'P3 not on circle: {circle_eq(P3[0], P3[1])}'

# 삼각형 넓이
def triangle_area(p1, p2, p3):
    return 0.5 * abs((p2[0]-p1[0])*(p3[1]-p1[1]) - (p3[0]-p1[0])*(p2[1]-p1[1]))

S = triangle_area(P1, P2, P3)
result = a * S

assert abs(S - 16*np.sqrt(2)) < 1e-10, f'Area incorrect: {S}'
assert abs(result - 32) < 1e-10, f'Answer incorrect: {result}'

print('VERIFY_PASS')