import numpy as np

k = 3
alpha = np.arcsin(k / (2*np.sqrt(3)))
a = 4*alpha / np.pi

Ax, Ay = a, k
Bx, By = 4-a, k
Cx, Cy = 4+a, -k
Dx, Dy = 8-a, -k

# 원래 함수 f(x) = 2sqrt(3)*sin(pi*x/4) 에 역대입 검증
def f(x):
    return 2*np.sqrt(3)*np.sin(np.pi*x/4)

assert abs(f(Ax) - k) < 1e-9, 'A not on y=k'
assert abs(f(Bx) - k) < 1e-9, 'B not on y=k'
assert abs(f(Cx) - (-k)) < 1e-9, 'C not on y=-k'
assert abs(f(Dx) - (-k)) < 1e-9, 'D not on y=-k'

# 기울기 검증
slope_AC = (Cy - Ay) / (Cx - Ax)
assert abs(slope_AC - (-3/2)) < 1e-9, f'slope={slope_AC}'

# 넓이 (shoelace)
verts = [(Ax,Ay),(Cx,Cy),(Dx,Dy),(Bx,By)]
n = len(verts)
area = 0
for i in range(n):
    j = (i+1) % n
    area += verts[i][0]*verts[j][1]
    area -= verts[j][0]*verts[i][1]
area = abs(area)/2

assert abs(area - 8) < 1e-9, f'area={area}'
print('VERIFY_PASS')
