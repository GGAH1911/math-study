import numpy as np

# 쌍곡선: y^2/9 - x^2/7 = 1, 초점 F(0,4), F'(0,-4)
F  = np.array([0.0,  4.0])
Fp = np.array([0.0, -4.0])

# 답: PF=9, PF'=15 → P 좌표 역산
# PF^2:  x0^2 + (y0-4)^2 = 81
# PF'^2: x0^2 + (y0+4)^2 = 225
# 빼면 16*y0 = 144 → y0 = 9
# x0^2 = 81 - 25 = 56
y0 = 9.0
x0 = np.sqrt(56.0)
P  = np.array([x0, y0])

# 1) P가 원래 쌍곡선 위에 있는지 (x^2/7 - y^2/9 = -1)
hyp_check = x0**2/7 - y0**2/9   # should be -1
assert abs(hyp_check - (-1)) < 1e-9, f'쌍곡선 불만족: {hyp_check}'

# 2) 거리 확인
PF_  = np.linalg.norm(P - F)
PFp_ = np.linalg.norm(P - Fp)
assert abs(PF_  -  9) < 1e-8, f'PF={PF_}'
assert abs(PFp_ - 15) < 1e-8, f"PF'={PFp_}"

# 3) |PF' - PF| = 2a = 6
assert abs(abs(PFp_ - PF_) - 6) < 1e-8, '쌍곡선 정의 위반'

# 4) 각의 이등분선이 (0,1)을 통과하는지
#    P에서 F, F' 방향 단위벡터 합 = 이등분선 방향
u1 = (F  - P) / np.linalg.norm(F  - P)
u2 = (Fp - P) / np.linalg.norm(Fp - P)
bisector = u1 + u2

Q  = np.array([0.0, 1.0])
PQ = Q - P
# PQ와 bisector가 평행이면 (0,1)이 이등분선 위에 있음
cross = PQ[0]*bisector[1] - PQ[1]*bisector[0]
assert abs(cross) < 1e-8, f'이등분선 불통과: cross={cross}'

# 5) 최종 답 확인
total = PF_ + PFp_
if abs(total - 24) < 1e-6:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: FP+F\'P={total}')
