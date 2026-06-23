import sympy as sp
# 파라미터화: 타원 x²/A2 + y²/B2 = 1, 원 중심 (cx,cy) 반지름 R.
# 직선 F'P가 타원과 만나는 점 Q(y>0). PQ+FQ 최댓값.
# 핵심: Q는 타원 위 → QF+QF'=2a. P가 F'와 Q 사이 → PQ+FQ = (F'Q+FQ)-F'P = 2a - F'P.
#   따라서 F'P 최소일 때 최대 = 2a - (|F'-중심| - R).
A2, B2 = 49, 33
cx, cy, R = 0, 3, 2
CANDIDATE = 11
a = sp.sqrt(A2)
c = sp.sqrt(A2 - B2)            # 초점거리
Fp = sp.Matrix([-c, 0])
center = sp.Matrix([cx, cy])
dist_Fp_center = sp.sqrt((center - Fp).dot(center - Fp))
FpP_min = dist_Fp_center - R    # F'에서 원 위 점까지 최소거리
ans = sp.nsimplify(2*a - FpP_min)
print('VERIFY_PASS' if ans == CANDIDATE else 'VERIFY_FAIL')
