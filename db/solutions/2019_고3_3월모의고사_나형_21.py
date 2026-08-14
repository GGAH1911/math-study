import sympy as sp

# ============================================================
# 원문제 (2019 고3 3월모의고사 나형 21번, 정답 ①)
#   함수 y = 2√x 의 그래프 위를 움직이는 점 P와 직선 y = x + 2 위를
#   움직이는 점 Q에 대하여 선분 PQ의 중점을 M이라 하자.
#   점 M과 점 A(0, 8) 사이의 거리의 최솟값은?
#
# 수학 구조 일반화
#   곡선 y = k√x (k>0), 직선 y = x + b (기울기 1), 점 A(0, a).
#   P=(p, k√p), Q=(q, q+b) (q ∈ ℝ 자유) 라 하면
#     M = ((p+q)/2, (k√p+q+b)/2)
#   p를 고정하면 q가 움직일 때 M은 기울기 1인 직선
#     y = x + c(p),  c(p) = (k√p - p + b)/2
#   위를 완전히 채우므로, A에서 이 직선까지의 (perp.) 거리가
#     d(p) = |c(p) - a| / √2
#   이고 이것이 "P를 p로 고정했을 때의 M-A 최소거리"이다.
#   c(p)는 p>0에서 유일한 임계점 p0 (dc/dp=0, 즉 k/(2√p)=1 → p0=k²/4)에서
#   최댓값을 가지는 오목함수이므로, a가 충분히 커서 c(p0) < a 이면
#   (=2a - b - k²/4 > 0) |c(p)-a|의 전역 최솟값도 p=p0 에서 나온다.
#   이때 최소거리 = (2a - b - k²/4) / (2√2).
#
# 파라미터로 뽑은 것 (모두 sympy 계산 결과인 '답'을 실제로 바꿈):
#   k : 곡선 y=k√x 의 계수
#   b : 직선 y=x+b 의 y절편
#   a : 점 A(0,a) 의 y좌표
#
# 보기(선택지) 구조
#   원문제 보기는 모두 (정수)·√2/8 꼴의 인접한 다섯 값
#     26,27,28,29,30  (단위: √2/8)   ← 정답이 그중 가장 작은 값(①)
#   이는 "정답 값 바로 위로 촘촘히 붙은 근접 오답"을 배치하는 전형적 구성이다.
#   일반화된 (k,b,a)에서도 최솟값을 m·√2/8 (m: 정수)로 나타낸 뒤,
#   m이 속하는 5-정수 연속 구간에서 m이 차지하는 위치 pos = (m-1) mod 5
#   를 그대로 보기 내 정답 위치로 사용한다 (원문제에서 m=26 → pos=0=①,
#   즉 이 식은 원문제의 실제 보기 배치를 그대로 재현하는 공식이다).
#   pos는 m(=파라미터들의 함수)이 바뀌면 함께 바뀌므로, k/b/a를 바꾸면
#   선택지 안에서 정답의 번호 자체도 실제로 달라진다.
# ============================================================

CANDIDATE = 1  # ★ 원문제 정답 (선지 번호) — 절대 바꾸지 않음

PARAMS = dict(
    k=sp.Integer(2),   # 곡선 y = k*sqrt(x) 의 계수
    b=sp.Integer(2),   # 직선 y = x + b 의 y절편
    a=sp.Integer(8),   # 점 A(0, a)
)


def _critical_p(k, b):
    """c(p) = (k√p - p + b)/2 의 임계점(=최댓값 위치) p0 를 실제로 미분/방정식 풀이로 구한다."""
    p = sp.symbols('p', positive=True)
    cp = (k * sp.sqrt(p) - p + b) / 2
    dcp = sp.diff(cp, p)
    sols = sp.solve(sp.Eq(dcp, 0), p)
    sols = [s for s in sols if sp.simplify(s).is_real and sp.simplify(s) > 0]
    if not sols:
        raise ValueError("양의 임계점이 존재하지 않습니다 (k>0 조건 위반 가능).")
    return p, cp, sols[0]


def value(prm):
    """실제 sympy 미분/최적화로 M과 A 사이 최소거리를 구한다."""
    k, b, a = prm['k'], prm['b'], prm['a']
    if k <= 0:
        raise ValueError("k는 양수여야 합니다 (곡선 y=k√x 가 정의되려면).")

    p, cp, p0 = _critical_p(k, b)
    gap = sp.simplify(cp.subs(p, p0) - a)  # c(p0) - a
    if not (gap.is_real and gap < 0):
        raise ValueError(
            "2a - b - k^2/4 > 0 조건이 깨져 임계점이 최소거리를 주지 않습니다 "
            "(A가 곡선/직선에서 충분히 멀리 있어야 함)."
        )
    dist = sp.simplify(sp.Abs(gap) / sp.sqrt(2))
    return dist


def choices(prm):
    """value(prm)을 (정수)*sqrt(2)/8 단위로 표현해, 그 정수가 속한 5-연속 구간을 보기로 만든다."""
    unit = sp.sqrt(2) / 8
    v = value(prm)
    m = sp.nsimplify(sp.simplify(v / unit))
    if not m.is_Integer or m <= 0:
        raise ValueError("정답 값이 √2/8의 정수배로 떨어지지 않아 원문제 보기 구조를 재현할 수 없습니다.")
    m = int(m)
    pos = (m - 1) % 5          # 원문제(m=26)에서 pos=0 이 되도록 만든, 값에서 유도된 위치 공식
    start = m - pos
    return tuple(sp.Rational(start + i) * unit for i in range(5))


def solve(prm):
    v = value(prm)
    ch = choices(prm)
    for idx, c in enumerate(ch):
        if sp.simplify(c - v) == 0:
            return idx + 1
    raise ValueError("정답 값이 유도된 보기 목록 안에 없습니다.")


def statement(prm):
    k, b, a = prm['k'], prm['b'], prm['a']
    return (
        f"그림과 같이 함수 y={k}\\sqrt{{x}}의 그래프 위를 움직이는 점 P와 직선 y=x+{b} 위를 "
        f"움직이는 점 Q에 대하여 선분 PQ의 중점을 M이라 하자. 점 M과 점 A(0, {a}) 사이의 "
        f"거리의 최솟값은? [4점]"
    )


if __name__ == '__main__':
    # 원문제 보기 값 고정 확인 (26,27,28,29,30 단위 √2/8)
    orig = (
        sp.Rational(13, 4) * sp.sqrt(2),
        sp.Rational(27, 8) * sp.sqrt(2),
        sp.Rational(7, 2) * sp.sqrt(2),
        sp.Rational(29, 8) * sp.sqrt(2),
        sp.Rational(15, 4) * sp.sqrt(2),
    )
    ch = choices(PARAMS)
    assert all(sp.simplify(ch[i] - orig[i]) == 0 for i in range(5)), "보기 목록이 원문제와 다름"

    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
