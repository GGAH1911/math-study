import sympy as sp

# 원문제: 매개변수 t(t>0)로 나타난 함수 x = t^2 + ln t, y = t^3 + 6t 에서
#         t=1일 때 dy/dx = (dy/dt)/(dx/dt) 의 값을 구하는 5지선다 문제.
# 수학 구조:
#   x(t) = p*t^2 + a*ln(t)   ... x를 이루는 두 항의 계수 p, a
#   y(t) = b*t^3 + c*t       ... y를 이루는 두 항의 계수 b, c
#   dy/dx|_{t=t0} = (3b*t0^2 + c) / (2p*t0 + a/t0)  를 t=t0 에서 계산.
#   보기 ①~⑤ = choice_base, choice_base+step, ..., choice_base+4*step 인 등차수열이고
#   (원문제는 1, 3/2, 2, 5/2, 3 → base=1, step=1/2),
#   실제 계산된 값이 이 등차수열의 몇 번째 항인지가 정답 번호가 된다.
#   → p, a, b, c, t0 를 바꾸면 dy/dx 값이 달라지고, 그 값이 보기 수열 중 어느 위치에
#     오는지도 바뀌므로 정답 번호가 실제로 바뀐다. (아래에서 p, c 를 각각 단독으로
#     바꿔도 정답이 바뀜을 직접 확인함)

CANDIDATE = 5  # ★원문제 정답: ⑤

PARAMS = dict(
    p=sp.Integer(1),           # x(t) 의 t^2 항 계수
    a=sp.Integer(1),           # x(t) 의 ln(t) 항 계수
    b=sp.Integer(1),           # y(t) 의 t^3 항 계수
    c=sp.Integer(6),           # y(t) 의 t 항 계수
    t0=sp.Integer(1),          # dy/dx 를 구할 t 값
    choice_base=sp.Rational(1),      # 보기 ①번 값
    choice_step=sp.Rational(1, 2),   # 보기 사이 공차
)


def value(prm):
    """x=p t^2+a ln t, y=b t^3+c t 에서 t=t0 일 때 dy/dx 를 sympy 로 실제 계산."""
    t = sp.Symbol('t', positive=True)
    p, a, b, c, t0 = prm['p'], prm['a'], prm['b'], prm['c'], prm['t0']

    x = p * t**2 + a * sp.ln(t)
    y = b * t**3 + c * t
    dx_dt = sp.diff(x, t)
    dy_dt = sp.diff(y, t)

    dx_val = dx_dt.subs(t, t0)
    if sp.simplify(dx_val) == 0:
        raise ValueError(f"t=t0={t0} 에서 dx/dt=0 이 되어 dy/dx 가 정의되지 않음")

    return sp.nsimplify(sp.simplify((dy_dt / dx_dt).subs(t, t0)))


def choices(prm):
    """보기 ①~⑤ = choice_base, choice_base+step, ..., choice_base+4*step 인 등차수열."""
    base = prm['choice_base']
    step = prm['choice_step']
    return [base + i * step for i in range(5)]


def solve(prm):
    """dy/dx 값을 실제로 계산한 뒤, 그 값이 보기 등차수열 중 몇 번째(1~5)인지 판정."""
    v = value(prm)
    base = prm['choice_base']
    step = prm['choice_step']

    idx = (v - base) / step
    if idx.q != 1:
        raise ValueError(f"계산된 dy/dx={v} 가 보기 등차수열(공차 {step}) 위에 있지 않음")
    idx0 = int(idx)
    if idx0 < 0 or idx0 >= 5:
        raise ValueError(f"계산된 dy/dx={v} 가 보기 범위 밖에 있어 문제로 성립하지 않음")

    return idx0 + 1


def _fmt_coef(coef, var):
    """계수를 자연스러운 문자열로 (1은 생략, -1은 -로)."""
    if coef == 1:
        return var
    if coef == -1:
        return f"-{var}"
    return f"{coef}{var}"


def statement(prm):
    p, a, b, c, t0 = prm['p'], prm['a'], prm['b'], prm['c'], prm['t0']
    x_str = f"{_fmt_coef(p, 't^2')} + {_fmt_coef(a, chr(92) + 'ln t')}"
    y_str = f"{_fmt_coef(b, 't^3')} + {_fmt_coef(c, 't')}"
    return (
        f"매개변수 t (t > 0)으로 나타내어진 함수 "
        f"x = {x_str}, y = {y_str} 에서 t = {t0}일 때, "
        f"\\frac{{dy}}{{dx}}의 값은?"
    )


# 원문제 보기와 정확히 일치하는지 고정
_cs = choices(PARAMS)
assert _cs == [sp.Rational(1), sp.Rational(3, 2), sp.Rational(2),
               sp.Rational(5, 2), sp.Rational(3)], _cs

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
