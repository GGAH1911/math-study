# 포물선 y^2=4px (초점 F(p,0), 준선 x=-p). cos∠PFF'=1/5 인 제1사분면 점 P.
# R = PF' 의 중점. 초점 O, F' 이고 R 을 지나는 쌍곡선. 선분 PF' 과 쌍곡선의 R 아닌 교점 Q.
# ★도형 전체가 p 에 비례하므로 p=1 로 풀어 둘레를 구한 뒤 p0 = 14/(둘레) 로 되돌린다.
#   넓이는 p^2 에 비례하므로 S^2 은 p^4 배가 된다.
CANDIDATE = 216
import sympy as sp

t = sp.symbols('t', real=True)
r = sp.symbols('r', positive=True)
Px, Py = 1 - r/5, r*sp.Rational(2, 5)*sp.sqrt(6)      # cos=1/5, sin=2√6/5
r0 = sp.solve(sp.Eq(Px + 1, r), r)[0]                  # 초점거리 = x+p
Pp = sp.Matrix([sp.simplify(Px.subs(r, r0)), sp.simplify(Py.subs(r, r0))])
assert sp.simplify(Pp[1]**2 - 4*Pp[0]) == 0            # 포물선 위 확인
F2, O = sp.Matrix([-1, 0]), sp.Matrix([0, 0])
Rp = (Pp + F2)/2
d = lambda A, B: sp.sqrt(sp.simplify((A - B).dot(A - B)))
gap = sp.simplify(d(Rp, O) - d(Rp, F2))                # R 의 부호 있는 차 (= -2a)
X = F2 + t*(Pp - F2)
sols = sp.solve(sp.Eq(sp.simplify(d(X, O) - d(X, F2)), gap), t)
cand = [s for s in sols if s.is_real and 0 < s < 1 and sp.simplify(s - sp.Rational(1, 2)) != 0]
if not cand:                                            # 다른 가지(부호 반대)
    sols = sp.solve(sp.Eq(sp.simplify(d(X, O) - d(X, F2)), -gap), t)
    cand = [s for s in sols if s.is_real and 0 < s < 1 and sp.simplify(s - sp.Rational(1, 2)) != 0]
Qp = X.subs(t, cand[0])
per1 = sp.simplify(d(Qp, O) + d(O, Rp) + d(Rp, Qp))    # p=1 일 때 둘레
p0 = sp.simplify(14/per1)
S1 = sp.Rational(1, 2)*sp.Abs(Pp[0]*Rp[1] - Pp[1]*Rp[0])
val = sp.simplify((S1*p0**2)**2)
print('VERIFY_PASS' if sp.simplify(val - CANDIDATE) == 0 else 'VERIFY_FAIL')
