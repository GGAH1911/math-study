"""2019 고3 3월모의고사 가형 27번 — 파라미터 솔버 (수동 작성).
문제: 직선 y=2 가 두 곡선 y=log2(4x), y=log2(x) 와 만나는 점 A, B.
      직선 y=k(k>2) 가 두 곡선과 만나는 점 C, D. B 지나 y축 평행선이 CD와
      만나는 점 E 가 CD를 1:2 내분. 사각형 ABDC 넓이 S → 12S. (답 54)
구조: log2(4x)=log2(x)+2 (상수차 shift=2). y=y0 에서 A=(2^{y0-shift},y0), B=(2^{y0},y0).
      y=k 에서 C=(2^{k-shift},k), D=(2^k,k). E_x=x_B 이고 CE:ED=1:2 →
      2^{y0} = x_C + (1/3)(x_D - x_C) → t=2^k 로 풀면 t/2=4 → k=3.
      ABDC 는 두 평행선 y=y0, y=k 사이 사다리꼴: S=½(AB+CD)(k-y0)=4.5 → 12S=54.
재생산: (shift, y0, 내분비, 배수) 파라미터화.
"""
import sympy as sp


def solve(shift, y0, ratio_num, ratio_den, mult):
    t = sp.symbols('t', positive=True)        # t = 2^k
    xA = sp.Integer(2) ** (y0 - shift)
    xB = sp.Integer(2) ** y0
    xC, xD = t / 2 ** shift, t                 # C,D 의 x좌표 (k에 대해)
    f = sp.Rational(ratio_num, ratio_num + ratio_den)
    t0 = sp.solve(sp.Eq(xB, xC + f * (xD - xC)), t)[0]
    k0 = sp.log(t0, 2)
    AB = xB - xA
    CD = (xD - xC).subs(t, t0)
    S = sp.Rational(1, 2) * (AB + CD) * (k0 - y0)
    return sp.simplify(mult * S)


CANDIDATE = 54
assert solve(2, 2, 1, 2, 12) == CANDIDATE, solve(2, 2, 1, 2, 12)
print('VERIFY_PASS')
