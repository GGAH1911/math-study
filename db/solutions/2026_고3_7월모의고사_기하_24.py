"""2026 고3 7월 기하 24 — 포물선 y^2 = 4p(x-h) 위의 점 (a, y0)과 준선 사이의 거리 (객관식)

구조: 점이 포물선 위에 있다는 조건으로 a 를 정하고, 준선 x = h - p 까지의 거리를 구한 뒤
      보기 목록과 대조해 보기 번호를 답한다.  (거리 = y0^2/(4p) + p, h 와는 무관)
"""
import sympy as sp

CANDIDATE = 2  # 정답 보기 번호 ② (값 5)

PARAMS = dict(
    p=1,                        # 포물선 y^2 = 4p(x-h) 의 p (꼭짓점-초점 거리)
    h=3,                        # 꼭짓점의 x좌표 (y^2 = 4(x-3) → h=3)
    y0=4,                       # 포물선 위의 점 (a, y0) 의 y좌표
    choices=(3, 5, 7, 9, 11),   # 보기 ①~⑤ 의 값
)


def solve(prm):
    """조건 → 답(보기 번호). 보기에 값이 없으면 0(해당 없음)."""
    p = sp.Rational(prm['p'])
    h = sp.Rational(prm['h'])
    y0 = sp.Rational(prm['y0'])

    a = sp.symbols('a', real=True)
    # 점 (a, y0) 이 포물선 y^2 = 4p(x-h) 위에 있다
    a_val = sp.solve(sp.Eq(y0**2, 4 * p * (a - h)), a)[0]

    directrix_x = h - p                       # 준선 x = h - p
    dist = sp.Abs(a_val - directrix_x)        # 점에서 준선(수직선)까지의 거리

    for i, c in enumerate(prm['choices'], 1):
        if sp.simplify(sp.nsimplify(c) - dist) == 0:
            return i
    return 0


def statement(prm):
    """새 문제 문장."""
    p, h, y0 = prm['p'], prm['h'], prm['y0']
    inner = f'x-{h}' if h > 0 else (f'x+{-h}' if h < 0 else 'x')
    marks = '①②③④⑤'
    opts = ' '.join(f'{marks[i]} {c}' for i, c in enumerate(prm['choices']))
    return (f'포물선 y^{{2}}={4*p}({inner}) 위의 점 (a,{y0})와 포물선의 준선\n'
            f'사이의 거리는? [3점]\n{opts}')


def value(prm):
    """참고용: 보기 번호가 아닌 실제 거리 값."""
    p, y0 = sp.Rational(prm['p']), sp.Rational(prm['y0'])
    return sp.simplify(y0**2 / (4 * p) + p)


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
