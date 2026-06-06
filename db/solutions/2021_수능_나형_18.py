#!/usr/bin/env python3
"""나형_18 역검산 — 지수/로그 합답형 (1/4<a<1).
직선 y=1·y=-1 이 두 곡선 y=log_a x, y=log_{4a} x 와 만나는 점:
  A=(a,1) B=(4a,1) C=(1/a,-1) D=(1/(4a),-1).
보기 ㄱ·ㄴ·ㄷ 진위를 원식으로 직접 판정 → 정답 ③(ㄱ,ㄴ)인지 확인."""
import sympy as sp

a = sp.Symbol('a', positive=True)
A = (a, sp.Integer(1)); B = (4 * a, sp.Integer(1))
C = (1 / a, sp.Integer(-1)); D = (1 / (4 * a), sp.Integer(-1))

# ── ㄱ: 선분 AB를 1:4로 외분한 점 = (0,1)? ──
# 1:4 외분점 P = (1·B − 4·A)/(1 − 4) = (4A − B)/3
Px = sp.simplify((4 * A[0] - B[0]) / 3)
Py = sp.simplify((4 * A[1] - B[1]) / 3)
g = (Px == 0) and (Py == 1)

# ── ㄴ: 사각형 ABCD 가 직사각형 ⟺ a=1/2 ──
# A,B 는 y=1, C,D 는 y=-1 위 → AB·CD 는 수평. 직사각형이려면 BC 가 수직 = B,C 의 x 동일: 4a = 1/a
sols = sp.solve(sp.Eq(4 * a, 1 / a), a)        # a>0
n = (sols == [sp.Rational(1, 2)])

# ── ㄷ: "AB<CD 이면 1/2<a<1" (주장) ──
# AB = |4a − a| = 3a,  CD = |1/(4a) − 1/a| = 3/(4a).  AB<CD ⟺ a < 1/2.
# 주어진 1/4<a<1 에서 AB<CD ⟺ 1/4<a<1/2 → 주장(1/2<a<1)의 반례 존재 → ㄷ 거짓.
ABlen = sp.Abs(B[0] - A[0])
CDlen = sp.Abs(D[0] - C[0])
a_test = sp.Rational(2, 5)                      # 0.4 ∈ (1/4, 1/2)
counter = bool(ABlen.subs(a, a_test) < CDlen.subs(a, a_test)) and not (a_test > sp.Rational(1, 2))
c = not counter                                 # ㄷ 참 ⟺ 반례 없음

correct = ''.join(s for s, ok in [('ㄱ', g), ('ㄴ', n), ('ㄷ', c)] if ok)
opt = {'ㄱ': 1, 'ㄷ': 2, 'ㄱㄴ': 3, 'ㄴㄷ': 4, 'ㄱㄴㄷ': 5}.get(correct)
print('VERIFY_PASS' if opt == 3 else f'VERIFY_FAIL(correct={correct!r}, opt={opt})')
