# 다항함수 f 에 대하여 g(x) = (a x^2 + b x + c) f(x) 일 때, f(x0)·f'(x0) 값으로 g'(x0) 을 구한다.
# 곱의 미분법: g'(x) = (a x^2 + b x + c)' f(x) + (a x^2 + b x + c) f'(x)
#
# ★파라미터화 솔버(scripts/CLAUDE.md 규격): PARAMS 를 바꾸면 같은 유형의 새 문제와
#   검증된 답이 그대로 나온다. 원문제는 PARAMS 기본값으로 재현된다.
#   보기는 c0 부터 cd 간격의 등차 5개(①~⑤) — solve 가 계산한 값을 보기와 대조해 번호를 정한다.
CANDIDATE = 4
import sympy as sp

PARAMS = dict(
    a=1, b=2, c=0,        # 곱해지는 다항식 a x^2 + b x + c
    x0=1,                 # 미분계수를 묻는 점
    f0=2, fp0=1,          # 주어진 조건 f(x0), f'(x0)
    c0=5, cd=2,           # 보기 ①~⑤ = c0, c0+cd, ..., c0+4cd
)


def gprime(prm):
    """곱의 미분법으로 g'(x0) 을 실제로 계산한다(값은 박아 두지 않는다)."""
    x = sp.Symbol('x')
    f = sp.Function('f')
    poly = prm['a'] * x**2 + prm['b'] * x + prm['c']
    dg = sp.diff(poly * f(x), x)                       # (poly)' f(x) + poly f'(x)
    dg = dg.subs(sp.Derivative(f(x), x), prm['fp0'])   # f'(x) → f'(x0)
    dg = dg.subs(f(x), prm['f0'])                      # f(x)  → f(x0)
    return sp.nsimplify(sp.simplify(dg.subs(x, prm['x0'])))


def choices(prm):
    return [sp.nsimplify(prm['c0'] + i * prm['cd']) for i in range(5)]


def solve(prm):
    """계산한 g'(x0) 를 보기와 대조해 정답 '번호'를 돌려준다."""
    val = gprime(prm)
    ch = choices(prm)
    n = sp.nsimplify((val - ch[0]) / prm['cd'] + 1)    # 등차 보기에서 val 의 위치
    if not (n.is_Integer and 1 <= n <= 5) or sp.simplify(ch[int(n) - 1] - val) != 0:
        raise ValueError(f'계산값 {val} 이 보기 {ch} 에 없다 — 보기를 다시 잡아야 하는 변형')
    return sp.Integer(n)


def statement(prm):
    x = sp.Symbol('x')
    poly = str(sp.expand(prm['a'] * x**2 + prm['b'] * x + prm['c'])).replace('**', '^').replace('*', '')
    ch = ' '.join(f'{m} {v}' for m, v in zip('①②③④⑤', choices(prm)))
    return (f"다항함수 f(x)에 대하여 함수 g(x)를 g(x)=({poly})f(x) 라 하자. "
            f"f({prm['x0']})={prm['f0']}, f'({prm['x0']})={prm['fp0']} 일 때, "
            f"g'({prm['x0']})의 값은? {ch}")


print('VERIFY_PASS' if sp.simplify(solve(PARAMS) - CANDIDATE) == 0 else 'VERIFY_FAIL')
