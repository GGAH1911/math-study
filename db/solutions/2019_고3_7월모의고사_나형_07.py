"""2019 고3 7월모의고사 나형 7번 — 파라미터화 솔버.

문제 구조: 함수 y=f(x) 의 그래프에서
  - x < bp1 구간은 직선 f(x) = left_slope*x + left_intercept
    (원문제는 left_slope=0 인 수평선, 즉 lim_{x→bp1-} f(x) = left_intercept)
  - x > bp2 구간은 직선 f(x) = right_slope*x + right_intercept
    (원문제는 우하향 직선, 즉 lim_{x→bp2+} f(x) = right_slope*bp2 + right_intercept)
구하는 값은 lim_{x→bp1-} f(x) + lim_{x→bp2+} f(x).
각 구간의 기울기·절편·기준점(bp1, bp2)을 파라미터로 두고 sympy.limit 으로 실제 극한을
계산한다. 보기(선택지)는 그래프의 y축 표시 범위 [y_min, y_max] 에서 나오는 연속한 정수
5개로, y_min·y_max 도 파라미터화해 문항마다 보기 구간이 달라지도록 했다.
"""
import sympy as sp

x = sp.symbols('x')

CANDIDATE = 2          # ★원문제 정답 — 절대 바꾸지 않음 (②, 값 2와 동일)

PARAMS = dict(
    bp1=-2,              # 좌극한을 구하는 기준점
    bp2=1,               # 우극한을 구하는 기준점
    left_slope=0,        # bp1 좌측 직선의 기울기 (0이면 수평선)
    left_intercept=-1,   # bp1 좌측 직선의 y절편 → lim_{x→bp1-} f(x)
    right_slope=-2,      # bp2 우측 직선의 기울기
    right_intercept=5,   # bp2 우측 직선의 y절편
    y_min=1,             # 그래프 y축(보기) 표시 범위 하한
    y_max=5,             # 그래프 y축(보기) 표시 범위 상한
)


def value(prm):
    """두 한쪽극한의 합을 sympy.limit 으로 실제 계산한다."""
    bp1 = sp.nsimplify(prm['bp1'])
    bp2 = sp.nsimplify(prm['bp2'])
    left_expr = sp.nsimplify(prm['left_slope']) * x + sp.nsimplify(prm['left_intercept'])
    right_expr = sp.nsimplify(prm['right_slope']) * x + sp.nsimplify(prm['right_intercept'])
    l1 = sp.limit(left_expr, x, bp1, '-')
    l2 = sp.limit(right_expr, x, bp2, '+')
    return sp.nsimplify(l1 + l2)


def choices(prm):
    """y_min부터 y_max까지의 연속한 정수 보기 목록 (값에서가 아니라 그래프 축 범위에서 유도)."""
    y_min = int(prm['y_min'])
    y_max = int(prm['y_max'])
    return tuple(range(y_min, y_max + 1))


def solve(prm):
    v = value(prm)
    if not v.is_number or v.has(sp.zoo, sp.nan, sp.oo, sp.I):
        raise ValueError(f'유효하지 않은 극한값: {v}')
    ch = choices(prm)
    if v not in ch:
        raise ValueError(f'값 {v} 이 보기 범위 {ch} 밖에 있음 — 문제로 성립하지 않음')
    return ch.index(v) + 1


def statement(prm):
    def lin_desc(slope, intercept, cond):
        if slope == 0:
            return f'{cond}일 때 f(x) = {intercept} (수평선)'
        return f'{cond}일 때 f(x) = {slope}x + {intercept}'

    left_txt = lin_desc(prm['left_slope'], prm['left_intercept'], f"x < {prm['bp1']}")
    right_txt = lin_desc(prm['right_slope'], prm['right_intercept'], f"x > {prm['bp2']}")
    opts = ' '.join(f'{i+1} {c}' for i, c in enumerate(choices(prm)))
    return (
        f"함수 y=f(x)의 그래프가 그림과 같다. {left_txt}, {right_txt}이다.\n"
        f"lim_(x→{prm['bp1']}-) f(x) + lim_(x→{prm['bp2']}+) f(x)의 값은? [3점]\n"
        f"보기: {opts}"
    )


# 원문제(=PARAMS) 기준 보기 목록이 실제 문제(①1 ②2 ③3 ④4 ⑤5)와 일치하는지 고정
assert choices(PARAMS) == (1, 2, 3, 4, 5)

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
