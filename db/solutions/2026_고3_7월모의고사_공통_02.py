"""2026 고3 7월모의고사 공통 2번 — 미분계수의 정의.

f(x) = a*x^2 + b*x + c 에 대하여 lim_{h->0} (f(x0+h) - f(x0))/h = f'(x0) 의 값을
보기에서 고르는 유형. PARAMS 의 계수·기준점·보기를 바꾸면 같은 유형의 새 문제가 된다.
"""
import sympy as sp

CANDIDATE = 2

PARAMS = dict(
    a=1,                          # f(x) = a x^2 + b x + c 의 x^2 계수
    b=3,                          # x 계수
    c=-1,                         # 상수항
    x0=3,                         # 극한을 잡는 점 lim_{h->0} (f(x0+h)-f(x0))/h
    choices=[7, 9, 11, 13, 15],   # 5지선다 보기 값 (정답 번호는 solve 가 대조해서 정한다)
)


def limit_value(prm):
    """미분계수의 정의 그대로 극한을 계산한다."""
    x, h = sp.symbols('x h')
    f = prm['a'] * x**2 + prm['b'] * x + prm['c']
    return sp.simplify(sp.limit((f.subs(x, prm['x0'] + h) - f.subs(x, prm['x0'])) / h, h, 0))


def solve(prm):
    """조건 → 정답 보기 번호. 계산값이 보기에 없으면 0(문항 미성립)."""
    v = sp.nsimplify(limit_value(prm))
    for i, t in enumerate(prm['choices'], 1):
        if sp.simplify(sp.nsimplify(t) - v) == 0:
            return i
    return 0


def statement(prm):
    x = sp.symbols('x')
    f = sp.nsimplify(prm['a']) * x**2 + sp.nsimplify(prm['b']) * x + sp.nsimplify(prm['c'])
    marks = ['①', '②', '③', '④', '⑤']
    opts = ' '.join(f'{m} {t}' for m, t in zip(marks, prm['choices']))
    return (f"함수 f(x)={sp.printing.sstr(f)}에 대하여 "
            f"lim_{{h→0}} (f({prm['x0']}+h)-f({prm['x0']}))/h 의 값은? [2점]\n{opts}")


def make_choices(prm, step=2, shift=1):
    """계산값을 포함하는 등차 보기 5개를 만든다(유사문제 생성용)."""
    v = sp.nsimplify(limit_value(prm))
    return [v + step * (k - shift) for k in range(5)]


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
