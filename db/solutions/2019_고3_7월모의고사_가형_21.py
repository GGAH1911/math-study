"""
2020년대 고3 모의고사 미적분/수학Ⅱ 계열 문항 파라미터화 솔버.

[문제 구조]
  0 < x < pi/2 에서 f(x) = sin x. 직선 y = t (0<t<1) 과 y=f(x) 의 교점을 P 라 하면
  x_P = arcsin(t), f'(x_P) = sqrt(1-t^2). 점 P에서의 접선의 x절편이 g(t) 이고,
  g'(t0) 값을 구하는 문제 (t0 는 특정 실수).

  g(t)  = arcsin(t) - t / sqrt(1-t^2)                (접선의 x절편, sympy 로 직접 미분)
  g'(t) = -t^2 / (1-t^2)^(3/2)

[파라미터화]
  원문제의 평가점 t0 = 2*sqrt(2)/3 은 sqrt(n^2-1)/n (n=3) 의 특수한 경우다.
  이를 일반화해 t0 = sqrt(n^2 - m) / n 로 두면 (0 < m < n^2 이어야 0<t0<1 실수),
    n=3, m=1  ->  t0 = sqrt(8)/3 = 2*sqrt(2)/3   (원문제와 동일)
  즉 n, m 두 정수가 t0 를 결정하고, 이는 g'(t0) 값을 실제로 바꾼다(둘 다 살아있는 파라미터).

  5지선다 보기는 g'(t0) 를 중심으로 공차 d 인 등차수열인데(원문제: 공차 4),
  정답이 몇 번째 보기에 오는지는 (n, m) 조합에 따라 달라지도록
  shift = (n+m-3) mod 5 로 정답 위치를 결정한다 — n=3,m=1 일 때 shift=1 이라
  ②(2번째) 가 정답이 되어 원문제(-28,-24,-20,-16,-12 중 ②=-24)를 정확히 재현한다.
  d 는 보기 간격(원문제 4)으로, 실제 보기 '값'은 바꾸지만 정답 '번호'는 안 바꾼다.
"""
import sympy as sp

CANDIDATE = 2  # 원문제 정답 보기 번호(②) — 절대 바꾸지 않음

PARAMS = dict(n=3, m=1, d=4)
#   n, m : 평가점 t0 = sqrt(n^2-m)/n 을 결정 (원문제 t0 = 2*sqrt(2)/3, 즉 n=3,m=1)
#   d    : 5지선다 보기의 공차 (원문제 4)


def _t0(n, m):
    """평가점 t0 = sqrt(n^2-m)/n. 0<t0<1 (실수 접점) 이어야 문제가 성립한다."""
    if not (0 < m < n ** 2):
        raise ValueError(f'0 < m < n^2 조건이 깨졌습니다 (n={n}, m={m}) — 실수 접점이 없음')
    return sp.sqrt(n ** 2 - m) / n


def value(prm):
    """g'(t0) 를 sympy 로 직접 미분/대입해서 구한다."""
    n, m = prm['n'], prm['m']
    t = sp.Symbol('t', positive=True)
    g = sp.asin(t) - t / sp.sqrt(1 - t ** 2)   # 점 P=(x_P,t)에서의 접선의 x절편
    g_prime = sp.diff(g, t)
    t0 = _t0(n, m)
    val = sp.simplify(g_prime.subs(t, t0))
    if not val.is_number or val.has(sp.zoo, sp.nan, sp.oo, sp.I):
        raise ValueError(f'g\'(t0) 가 유효한 실수가 아닙니다: {val}')
    return val


def choices(prm):
    """5지선다 보기를 값(V)에서 유도한다. 원문제 ①-28 ②-24 ③-20 ④-16 ⑤-12 는
    공차 d(=4)인 등차수열이며, V(=-24)가 그 2번째 항이다. 정답이 몇 번째 항에
    오는지는 (n,m) 에서 유도한 shift 로 결정해, n·m 이 바뀌면 정답 번호도 바뀐다."""
    n, m, d = prm['n'], prm['m'], prm['d']
    V = sp.nsimplify(value(prm))
    shift = (n + m - 3) % 5   # 0-based: V가 놓일 위치
    return [sp.simplify(V + (i - shift) * d) for i in range(5)]


def solve(prm):
    """값이 보기 중 몇 번째(1-based)인지 반환 — 객관식 정답 번호."""
    V = sp.nsimplify(value(prm))
    for i, c in enumerate(choices(prm), 1):
        if sp.simplify(c - V) == 0:
            return i
    raise ValueError('값이 보기 목록 안에 없습니다')


def statement(prm):
    n, m, d = prm['n'], prm['m'], prm['d']
    t0_latex = sp.latex(sp.nsimplify(_t0(n, m)))
    return (
        f"0 < t < 1 인 실수 t 에 대하여 직선 y = t 와 함수 "
        f"f(x) = \\sin x \\left( 0 < x < \\frac{{\\pi}}{{2}} \\right) 의 그래프가 만나는 "
        f"점을 P 라 할 때, 곡선 y = f(x) 위의 점 P 에서 그은 접선의 x절편을 g(t) 라 하자. "
        f"g'\\left( {t0_latex} \\right) 의 값은? (보기는 공차 {d} 인 등차수열)"
    )


# 원문제 보기와 유도된 보기가 일치하는지 고정
assert [sp.nsimplify(c) for c in choices(PARAMS)] == [-28, -24, -20, -16, -12]

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
