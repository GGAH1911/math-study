"""2026 고3 7월 미적분 23번 — tan/지수 기본극한 결합 (파라미터화 솔버)

    lim_{x→0} tan(a x) / (e^{b x} - 1)  의 값은?  (객관식 5지선다)

수학 구조: 분자·분모를 x 로 나누면 (tan(ax)/x) → a, ((e^{bx}-1)/x) → b 이므로 답은 a/b.
solve 는 그 값을 sympy 극한으로 실제 계산한 뒤 보기 목록과 대조해 **보기 번호**를 돌려준다.
"""
from sympy import symbols, tan, exp, limit, nsimplify

CANDIDATE = 3

PARAMS = dict(
    a=6,                       # 분자 tan(a x) 의 계수
    b=2,                       # 분모 e^{b x} - 1 의 계수
    choices=[1, 2, 3, 4, 5],   # 보기 ①~⑤ 의 값 (정답 번호는 solve 가 계산한다)
)


def limit_value(prm):
    """문제의 극한값 자체 (보기와 무관한 순수 계산)."""
    x = symbols('x')
    a, b = prm['a'], prm['b']
    return nsimplify(limit(tan(a * x) / (exp(b * x) - 1), x, 0))


def solve(prm=None):
    """조건 → 답(보기 번호). 값이 보기에 없으면 그 조합은 문제로 성립하지 않는다."""
    prm = PARAMS if prm is None else prm
    val = limit_value(prm)
    for i, c in enumerate(prm['choices'], start=1):
        if nsimplify(c) == val:
            return i
    raise ValueError(f'극한값 {val} 이(가) 보기 {prm["choices"]} 에 없다')


def statement(prm=None):
    """새 문제 문장(유사문제 재생성용)."""
    prm = PARAMS if prm is None else prm
    marks = '①②③④⑤'
    opts = ' '.join(f'{marks[i]} {c}' for i, c in enumerate(prm['choices']))
    return (f'\\lim_{{x→0}}\\frac{{\\tan {prm["a"]}x}}{{e^{{{prm["b"]}x}}-1}} 의 값은? [2점]\n'
            f'  {opts}')


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
