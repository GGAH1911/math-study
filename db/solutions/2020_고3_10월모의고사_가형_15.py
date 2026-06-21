from sympy import symbols, log, sqrt, solve, simplify, N

# 검증: a = √6/3일 때 모든 조건 만족
a_val = sqrt(6) / 3
p = -2
r = a_val ** p

P = (p, a_val ** p)
Q = (a_val ** p, p)
R = (r, -log(r, a_val))

# 기울기 검증
slope_PR = (R[1] - P[1]) / (R[0] - P[0])
print(f'기울기: {simplify(slope_PR)} (기댓값: 1/7)')

# 거리 검증
dist_PR = sqrt((R[0] - P[0])**2 + (R[1] - P[1])**2)
print(f'거리: {simplify(dist_PR)} (기댓값: 5√2/2)')

# QR이 수직인지 확인
if R[0] == Q[0]:
    print('QR은 수직 ✓')

# 기울기 -1 확인
slope_QP = (P[1] - Q[1]) / (P[0] - Q[0])
print(f'QP 기울기: {simplify(slope_QP)} (기댓값: -1)')

if abs(N(slope_PR - 1/7)) < 1e-10 and abs(N(dist_PR - 5*sqrt(2)/2)) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')