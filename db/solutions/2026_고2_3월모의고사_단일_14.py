import numpy as np

# 문제 원래 조건
# 원 C: (x-7)^2 + (y-3)^2 = 2, 중심 O=(7,3), 반지름 sqrt(2)
# A = (2, 0)
# Q on y=x, P on circle C
# 최솟값 후보: 4*sqrt(2)

A = np.array([2.0, 0.0])
Oc = np.array([7.0, 3.0])
r = np.sqrt(2)

# 최적 Q: (7/3, 7/3)
Q_opt = np.array([7/3, 7/3])

# Q가 y=x 위에 있는지 확인
assert abs(Q_opt[0] - Q_opt[1]) < 1e-10, 'Q not on y=x'

# 최적 P: Q에서 Oc 방향으로 원 위
direc = Oc - Q_opt
direc_norm = direc / np.linalg.norm(direc)
P_opt = Q_opt + (np.linalg.norm(direc) - r) * direc_norm

# P가 원 위에 있는지 확인
assert abs((P_opt[0]-7)**2 + (P_opt[1]-3)**2 - 2) < 1e-9, 'P not on circle'

val = np.linalg.norm(A - Q_opt) + np.linalg.norm(Q_opt - P_opt)
expected = 4 * np.sqrt(2)

# 다양한 Q, P로 브루트포스 최솟값 확인
min_val = float('inf')
for t in np.linspace(-20, 20, 100000):
    Q = np.array([t, t])
    dQOc = np.linalg.norm(Q - Oc)
    if dQOc < r:
        qp_min = 0.0
    else:
        qp_min = dQOc - r
    total = np.linalg.norm(A - Q) + qp_min
    if total < min_val:
        min_val = total

if abs(min_val - expected) < 1e-6 and abs(val - expected) < 1e-6:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: computed min={min_val:.8f}, expected={expected:.8f}, val_at_opt={val:.8f}')
