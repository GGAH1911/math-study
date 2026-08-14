"""2019 고3 4월모의고사 가형 11번 — 파라미터화 솔버.

원문제: f(x)=2^x/3, g(x)=2^x-2. 두 곡선이 y축과 만나는 점 A=f(0), B=g(0),
곡선끼리의 교점 C(x좌표만 필요). 선분 AB(y축 위)를 밑변, C의 x좌표를 높이로 하는
삼각형 ABC의 넓이를 구하는 문제. (정답 ②: (2/3)log_2 3)

★ 파라미터화한 수학 구조
  f(x) = 2^x / d      (d: f의 분모, d>1)
  g(x) = 2^x - c      (c: g의 y절편을 낮추는 상수, c>0)

  A = f(0) = 1/d,  B = g(0) = 1-c            → 밑변 base = |A-B| = |1/d - 1 + c|
  교점 C: 2^x/d = 2^x - c → 2^x(1-1/d) = c → 2^x = c·d/(d-1) → x_C = log_2( c·d/(d-1) )
  넓이 value = (1/2)·base·x_C = K·x_C   (K := base/2, 유리수)

  d, c 두 값 모두 base(=K)와 x_C(=로그의 진수)를 통해 넓이 값을 바꾼다.
  → d 또는 c 어느 하나만 바뀌어도 value(prm)가 달라짐(아래 VARIANTS로 직접 확인).

★ 보기(선택지) 구조
  원문제 보기 ①~⑤는 x_C 단위로 정확히 1/3, 2/3, 3/3, 4/3, 5/3 배로 등간격 배치되어
  있다 (unit = x_C/3). 이는 원문제의 실제 보기 배치를 그대로 반영한 구조이며,
  value(prm) = i·unit 을 만족하는 i(1~5)가 바로 정답 번호다. 그런 i가 없으면
  (즉 이 d,c 조합으로는 5지선다 형태가 성립하지 않으면) 예외를 던진다.

  d,c는 "밑변/높이가 만들어내는 넓이가 x_C의 정수/3 배가 되어야 5지선다가 성립한다"는
  조건으로 서로 묶여 있다(자연수 조건과 유사한 정수해 제약) → VARIANTS로 여러 유효
  조합을 제시한다.
"""
import sympy as sp


def _core(d, c):
    """A,B,C 및 넓이 value를 계산. 정의역이 깨지면 예외."""
    d, c = sp.Rational(d), sp.Rational(c)
    if d == 1:
        raise ValueError("d=1이면 두 곡선이 평행/일치하여 교점이 정의되지 않음")
    arg = c * d / (d - 1)          # 2^x_C = arg 이어야 함
    if arg <= 0:
        raise ValueError(f"교점 조건 2^x=c·d/(d-1)={arg} <= 0 이라 실수해 x_C가 없음")
    x = sp.symbols('x', real=True)
    f, g = 2 ** x / d, 2 ** x - c
    A, B = f.subs(x, 0), g.subs(x, 0)
    base = sp.Abs(A - B)
    xc = sp.log(arg, 2)
    value = sp.simplify(sp.Rational(1, 2) * base * xc)
    return base, xc, value


def value(prm):
    _, _, v = _core(prm['d'], prm['c'])
    return v


def choices(prm):
    """보기 5개: x_C 단위(unit=x_C/3)의 1~5배. 원문제 보기와 정확히 일치."""
    _, xc, _ = _core(prm['d'], prm['c'])
    unit = xc / 3
    return [sp.simplify(i * unit) for i in range(1, 6)]


def solve(prm):
    v = value(prm)
    opts = choices(prm)
    for i, opt in enumerate(opts, start=1):
        if sp.simplify(opt - v) == 0:
            return i
    raise ValueError(f"value={v} 가 5지선다 보기(x_C의 1~5/3배) 안에 들지 않음: "
                      f"이 d,c 조합은 문제로 성립하지 않음")


def statement(prm):
    d, c = prm['d'], prm['c']
    return (
        f"그림과 같이 두 함수 f(x)=2^x/{d}, g(x)=2^x-{c}의 그래프가 y축과 만나는 "
        f"점을 각각 A, B라 하고, 두 곡선 y=f(x), y=g(x)가 만나는 점을 C라 할 때, "
        f"삼각형 ABC의 넓이는?"
    )


PARAMS = dict(d=3, c=2)          # 원문제: f=2^x/3, g=2^x-2

# 정답 번호(②) — 절대 바꾸지 않음
CANDIDATE = 2

# d, c 가 서로 묶여 있어(5지선다 성립 조건) 한쪽만 임의로 흔들 수 없으므로
# 유효한 (d,c) 조합을 여러 개 제시한다. 이 중 2개 이상은 원문제와 다른 답을 낸다.
VARIANTS = [
    dict(d=3, c=2),          # 원문제 → ②  (value = 2/3 log2 3)
    dict(d=3, c=sp.Rational(4, 3)),   # → ①  (value = 1/3 log2 2 = 1/3)
    dict(d=3, c=sp.Rational(8, 3)),   # → ③  (value = log2 4 = 2)
    dict(d=2, c=sp.Rational(7, 6)),   # → ①  (d도 바뀜: value = 1/3 log2(7/3))
]

if __name__ == '__main__':
    # 보기 목록이 원문제 보기와 정확히 같은지 고정
    orig_choices = choices(PARAMS)
    expected = [sp.Rational(i, 3) * sp.log(3, 2) for i in range(1, 6)]
    for a, b in zip(orig_choices, expected):
        assert sp.simplify(a - b) == 0, (a, b)

    results = [solve(v) for v in VARIANTS]
    assert len(set(results)) >= 3, results   # 서로 다른 답이 여러 개 나와야 함(파라미터가 답을 실제로 바꿈)
    assert results[0] == CANDIDATE

    print('variant answers:', results)
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
