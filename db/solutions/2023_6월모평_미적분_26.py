import math

def tri_area(p1, p2, p3):
    return 0.5 * abs(p1[0]*(p2[1]-p3[1]) + p2[0]*(p3[1]-p1[1]) + p3[0]*(p1[1]-p2[1]))

def circumcircle(p1, p2, p3):
    ax, ay = p1; bx, by = p2; cx, cy = p3
    d = 2 * (ax*(by - cy) + bx*(cy - ay) + cx*(ay - by))
    ux = ((ax**2 + ay**2)*(by - cy) + (bx**2 + by**2)*(cy - ay) + (cx**2 + cy**2)*(ay - by)) / d
    uy = ((ax**2 + ay**2)*(cx - bx) + (bx**2 + by**2)*(ax - cx) + (cx**2 + cy**2)*(bx - ax)) / d
    r = math.hypot(ax - ux, ay - uy)
    return (ux, uy), r

# 원 문제 조건: A1B1=2, B1A2=3, angle A1B1A2 = pi/3
B1 = (0.0, 0.0)
A2 = (3.0, 0.0)
A1 = (2*math.cos(math.pi/3), 2*math.sin(math.pi/3))
assert abs(math.dist(A1, B1) - 2) < 1e-9
assert abs(math.dist(B1, A2) - 3) < 1e-9
v1 = (A1[0]-B1[0], A1[1]-B1[1]); v2 = (A2[0]-B1[0], A2[1]-B1[1])
assert abs((v1[0]*v2[0]+v1[1]*v2[1])/(2*3) - 0.5) < 1e-9

# 원 O1 (삼각형 A1B1A2 외접원)
center1, r1 = circumcircle(A1, B1, A2)

# B2: A2 지나 A1B1에 평행한 직선이 O1과 만나는 다른 점
dx, dy = A1[0]-B1[0], A1[1]-B1[1]
cx, cy = center1
a, b = A2[0]-cx, A2[1]-cy
t = -2*(a*dx + b*dy)/(dx**2 + dy**2)
B2 = (A2[0] + t*dx, A2[1] + t*dy)
assert abs(math.dist(B2, center1) - r1) < 1e-9
# 평행 확인
cross = (B2[0]-A2[0])*dy - (B2[1]-A2[1])*dx
assert abs(cross) < 1e-9

# C1: 직선 A1B2 와 직선 B1A2(=x축) 교점
s = -A1[1] / (B2[1] - A1[1])
C1 = (A1[0] + s*(B2[0]-A1[0]), 0.0)

T1 = tri_area(A1, A2, C1) + tri_area(B1, C1, B2)

# 다음 단계: A3 (B2A3 || B1A2, |B2A3| = 3*(A2B2/A1B1))
scale = math.dist(A2, B2) / math.dist(A1, B1)
B2A3_len = 3 * scale
# B1A2 방향 = (1,0)
A3 = (B2[0] + B2A3_len, B2[1])
# 닮음 검증: angle A2B2A3 = pi/3
u1 = (A2[0]-B2[0], A2[1]-B2[1])
u2 = (A3[0]-B2[0], A3[1]-B2[1])
cos_chk = (u1[0]*u2[0]+u1[1]*u2[1])/(math.hypot(*u1)*math.hypot(*u2))
assert abs(cos_chk - 0.5) < 1e-9

# 원 O2
center2, r2 = circumcircle(A2, B2, A3)
assert abs(r2 - r1*scale) < 1e-9

# B3: A3 지나 A2B2에 평행한 직선이 O2와 만나는 다른 점
dx2, dy2 = B2[0]-A2[0], B2[1]-A2[1]
cx2, cy2 = center2
a2, b2 = A3[0]-cx2, A3[1]-cy2
t2 = -2*(a2*dx2 + b2*dy2)/(dx2**2 + dy2**2)
B3 = (A3[0] + t2*dx2, A3[1] + t2*dy2)

# C2: 직선 A2B3 와 직선 B2A3 교점
u = (B2[1]-A2[1])/(B3[1]-A2[1])
C2 = (A2[0] + u*(B3[0]-A2[0]), B2[1])

T2 = tri_area(A2, A3, C2) + tri_area(B2, C2, B3)
ratio = T2 / T1
assert abs(ratio - 0.25) < 1e-12

limit_S = T1 / (1 - ratio)
expected = 4*math.sqrt(3)/3
if abs(limit_S - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
