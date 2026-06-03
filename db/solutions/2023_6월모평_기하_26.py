import numpy as np

# 원래 조건: 타원 x^2/3 + y^2 = 1, 직선 y = x-1

def on_ellipse(p, tol=1e-9):
    return abs(p[0]**2/3 + p[1]**2 - 1) < tol

def on_line(p, tol=1e-9):
    return abs(p[1] - p[0] + 1) < tol

# 교점 A, C
A = np.array([3/2, 1/2])
C = np.array([0.0, -1.0])
assert on_ellipse(A) and on_line(A), 'A check failed'
assert on_ellipse(C) and on_line(C), 'C check failed'

# 최적 B, D
B = np.array([-3/2, 1/2])   # t = 5*pi/6, f(t)=-3 (B 쪽 최대 거리)
D = np.array([3/2, -1/2])   # t = -pi/6, f(t)=1  (D 쪽 최대 거리)
assert on_ellipse(B), 'B not on ellipse'
assert on_ellipse(D), 'D not on ellipse'

# 직선 AC: x-y-1=0까지의 거리
hB = abs(B[0]-B[1]-1)/np.sqrt(2)
hD = abs(D[0]-D[1]-1)/np.sqrt(2)
AC_len = np.linalg.norm(A-C)
area_formula = 0.5 * AC_len * (hB + hD)

# 신발끈 공식
def shoelace(pts):
    n = len(pts)
    s = sum(pts[i][0]*pts[(i+1)%n][1] - pts[(i+1)%n][0]*pts[i][1] for i in range(n))
    return abs(s)/2

area_shoelace = shoelace([A, B, C, D])

# 수치적 최댓값 확인 (타원 파라미터 t 전체 탐색)
t = np.linspace(0, 2*np.pi, 200001)
xt, yt = np.sqrt(3)*np.cos(t), np.sin(t)
ft = xt - yt - 1
mask_pos = ft > 0
mask_neg = ft < 0
hmax_D = np.max(ft[mask_pos]) / np.sqrt(2) if mask_pos.any() else 0
hmax_B = np.max(-ft[mask_neg]) / np.sqrt(2) if mask_neg.any() else 0
max_area_num = 0.5 * AC_len * (hmax_B + hmax_D)

if (abs(area_formula - 3) < 1e-9 and
    abs(area_shoelace - 3) < 1e-9 and
    abs(max_area_num - 3) < 1e-4):
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: formula={area_formula:.8f}, shoelace={area_shoelace:.8f}, num_max={max_area_num:.8f}')
