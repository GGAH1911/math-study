# -*- coding: utf-8 -*-
"""
[원문제] 2019 고3 10월 모의고사 가형 16번
  길이가 2인 선분 AB를 지름으로 하는 원 C1과 점 B를 중심으로 하고 원 C1 위의 점 P를
  지나는 원 C2가 있다. 원 C1의 중심 O에서 원 C2에 그은 두 접선의 접점을 Q, R이라 하자.
  ∠PAB = θ일 때 사각형 ORBQ의 넓이 S(θ)에 대해 lim_{θ→0+} S(θ)/θ 의 값은?
  [정답] ① 2  (보기: ①2 ②√3 ③1 ④√3/2 ⑤1/2)

[수학 구조 — 파라미터로 뽑은 것]
  좌표계: A=(0,0), B=(d,0). 원 C1은 AB를 지름으로 하므로 중심 O=(d/2,0), 반지름 d/2.
    - ∠PAB=θ 인 원 C1 위의 점 P: P=(d·cos²θ, d·sinθ·cosθ)  (θ→0+ 이면 P→B)
    - 원 C2: 중심 B, 반지름 r = |BP| = d·sinθ
    - 접선을 긋는 점 T(선분 AB 위, |TB|=b): 원문제는 T=O(중심)이므로 b=d/2
      ※ TQ ⟂ BQ(접선·반지름) 이므로 사각형 TRBQ 는 대각선 TB 로 나뉜 합동 직각삼각형
        두 개 → 넓이 S(θ) = r·√(b²−r²) = d·sinθ·√(b²−d²·sin²θ)
    - lim_{θ→0+} S(θ)/θ = d·b   (sinθ/θ → 1, √(b²−d²sin²θ) → b)
  즉 지름 d 와 접선 기준점의 위치 b 가 각각 답(=d·b)을 실제로 바꾸는 두 손잡이다.

  보기는 v·{1, √3/2, 1/2, √3/4, 1/4} 의 곱셈 비율 격자에서 유도한다(원문제
  v=2 → {2, √3, 1, √3/2, 1/2} 그대로). 정답의 보기 번호(=solve 반환값)는 값
  v=d·b 에서 유도한 offset 만큼 격자를 회전시켜 정한다 — 원문제(d=2,b=1)에서는
  offset=0 → 정답이 ①에 온다.
"""
import sympy as sp

CANDIDATE = 1  # ★원문제 정답: ① (값 2) — 절대 바꾸지 않음

PARAMS = dict(
    d=2,  # 선분 AB(원 C1의 지름)의 길이
    b=1,  # 접선을 긋는 점 T에서 B까지의 거리 |TB| (원문제: T=O=중심, b=d/2)
)


def value(prm):
    """수학적 답: lim_{θ→0+} S(θ)/θ 를 sympy 로 실제로 계산한다."""
    d = sp.nsimplify(prm['d'])
    b = sp.nsimplify(prm['b'])
    # 문제 성립 조건: 지름>0, T는 선분 AB 위(0 < b ≤ d) — 어기면 예외
    if d <= 0 or b <= 0 or b > d:
        raise ValueError(f'문제가 성립하지 않는 조합: d={d}, b={b} (0 < b ≤ d 필요)')

    th = sp.symbols('theta', real=True, positive=True)
    r = d * sp.sin(th)                    # |BP| = 원 C2의 반지름
    S = r * sp.sqrt(b**2 - r**2)          # 사각형 TRBQ(연)의 넓이
    return sp.simplify(sp.limit(S / th, th, 0, '+'))


def choices(prm):
    """보기 5개: 값 v 의 곱셈 비율 격자 v·{1, √3/2, 1/2, √3/4, 1/4} 를
    offset(=(v−2) mod 5) 만큼 회전. 원문제(d=2, b=1, v=2)면 offset=0 →
    [2, √3, 1, √3/2, 1/2] 로 원문제 보기가 그대로 나온다."""
    v = value(prm)
    ratios = [sp.Integer(1), sp.sqrt(3) / 2, sp.Rational(1, 2),
              sp.sqrt(3) / 4, sp.Rational(1, 4)]
    d, b = sp.nsimplify(prm['d']), sp.nsimplify(prm['b'])
    offset = int(d * b - 2) % 5           # 값에서 유도한 회전량
    rotated = ratios[offset:] + ratios[:offset]
    return [sp.simplify(v * r) for r in rotated]


def solve(prm):
    """보기 번호(1~5) 반환: value(prm) 이 choices(prm) 중 몇 번째인지."""
    v = value(prm)
    ch = choices(prm)
    for i, c in enumerate(ch, start=1):
        if sp.simplify(c - v) == 0:
            return i
    raise ValueError('정답이 보기 목록에 없음 — 유효하지 않은 파라미터 조합')


def statement(prm):
    """파라미터로 만들어진 문제 문장(한국어). b=d/2 면 원문제 그대로 '중심 O에서'."""
    d, b = prm['d'], prm['b']
    ch = choices(prm)
    marks = ['①', '②', '③', '④', '⑤']
    opts = '  '.join(f'{m} {c}' for m, c in zip(marks, ch))

    if sp.simplify(sp.nsimplify(b) - sp.nsimplify(d) / 2) == 0:
        source = '원 C₁의 중심 O에서 원 C₂에 그은 두 접선의 접점을 각각 Q, R이라 하자'
        quad = 'ORBQ'
    else:
        source = (f'선분 AB 위의 점 T(\\overline{{TB}}={b})에서 원 C₂에 그은 '
                  f'두 접선의 접점을 각각 Q, R이라 하자')
        quad = 'TRBQ'

    th_max = sp.asin(sp.Rational(b, d)) if b < d else sp.pi / 2
    return (
        f'그림과 같이 길이가 {d}인 선분 AB를 지름으로 하는 원 C₁과 점 B를 중심으로 하고 '
        f'원 C₁ 위의 점 P를 지나는 원 C₂가 있다. {source}. ∠PAB=θ일 때, '
        f'사각형 {quad}의 넓이를 S(θ)라 하자. '
        f'\\lim_{{\\theta \\to 0+}} \\frac{{S(\\theta)}}{{\\theta}}의 값은? '
        f'(단, 0 < θ < {sp.latex(th_max)}) [4점]\n{opts}'
    )


# ── 원문제 보기 재현 고정 (요구사항 4) ──
_ORIG = [sp.Integer(2), sp.sqrt(3), sp.Integer(1), sp.sqrt(3) / 2, sp.Rational(1, 2)]
_derived = choices(PARAMS)
assert len(_derived) == 5 and all(sp.simplify(_derived[i] - _ORIG[i]) == 0 for i in range(5)), \
    f'유도 보기가 원문제 보기와 다름: {_derived}'

# ── 파라미터 변이 자체검증 (요구사항 2): 각 손잡이를 바꾸면 답(보기 번호·값)이 실제로 달라진다 ──
assert value({**PARAMS, 'd': 3}) == 3 and solve({**PARAMS, 'd': 3}) != CANDIDATE
assert value({**PARAMS, 'b': 2}) == 4 and solve({**PARAMS, 'b': 2}) != CANDIDATE
assert value({**PARAMS, 'd': 4}) == 4 and solve({**PARAMS, 'd': 4}) != CANDIDATE

print(statement(PARAMS))
print()
print(f'lim S(θ)/θ = {value(PARAMS)}  →  정답 보기: {solve(PARAMS)}번')
print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
