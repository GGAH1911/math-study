# -*- coding: utf-8 -*-
"""
[원문제 구조]
  f'(x) = x*e^{-x^2}
  (가) g(x) = ∫_1^x f'(t)(x+1-t) dt
  (나) f(x) = g'(x) - f'(x)
  <보기> ㄱ. g'(1)=1/e   ㄴ. f(1)=g(1)   ㄷ. 어떤 양수 x에 대해 g(x)<f(x)
  → ② (ㄱ, ㄴ)

[수학적 구조 분석]
  라이프니츠 규칙으로 g'(x) = f(x) - f(1) + 1*f'(x) 가 항상 성립한다(적분 하한과
  (x+1-t)의 오프셋 "1"이 같은 값이기 때문). 조건 (나)와 비교하면 이 "1"(오프셋/하한)이
  f'(x) 앞의 계수 "1"과 반드시 일치해야만 항등식이 모든 x에서 성립하고, 그 결과
  f(하한)=0 이 강제된다. 이 구조 때문에 ㄱ, ㄴ은 파라미터를 바꿔도 "구조적으로 항상 참"
  이고, 오직 ㄷ(g(x)<f(x)를 만족하는 양수 x의 존재)만 실제로 변할 수 있는 명제다.

  ㄷ의 진위를 바꾸는 두 개의 독립적인 수학적 손잡이:
    a : 적분 하한/조건식의 기준점 (원문제는 a=1). h(x)=g(x)-f(x) 는 h'(x)=f(x),
        h(a)=0 을 만족하는데, f(t) 의 부호는 |t-b| 와 |a-b| 의 대소로 정해진다.
        a>0 이면 t>0 구간에서 h(x)>0 만 나와 ㄷ이 거짓이지만, a<0 이면 (0,|2b-a|) 부근에서
        h(x)<0 이 되어 ㄷ이 참으로 바뀐다.
    b : f'(x)=(x-b)e^{-k(x-b)^2} 의 대칭중심(원문제는 b=0, 즉 f'(x)=x e^{-x^2}).
        b 를 a 보다 크게 잡으면(예: a=1,b=3) t∈(a,b) 구간에서 f(t)<0 이 되어
        h(x)<0 인 양수 x가 생기고 ㄷ이 참으로 바뀐다.
  k : 지수 감쇠 계수(원문제는 k=1). ㄱ의 우변 수치(=a*f'(a))와 f,g 의 구체적 값을 바꾸지만
      부호구조(음수/양수 경계)는 바꾸지 않아 ㄷ의 참/거짓에는 영향이 없다 — 즉 "장식이
      아니라 값을 바꾸는" 파라미터지만 답을 바꾸는 주 손잡이는 a, b 이다.

  a, b 를 바꾸면 정말로 최종 정답(보기 선택)이 바뀌는지 아래 solve() 로 직접 검증했다.
"""

import sympy as sp

CANDIDATE = 2  # ★원문제 정답: ② ㄱ, ㄴ  (절대 변경 금지)

PARAMS = dict(
    a=1,   # 적분 하한이자 (가)식의 오프셋, (나)식의 계수와 자동으로 맞춰지는 기준점
    b=0,   # f'(x)=(x-b)e^{-k(x-b)^2} 의 대칭중심 (원문제: b=0 → f'(x)=x e^{-x^2})
    k=1,   # 지수 감쇠 계수 (원문제: k=1)
)

_x, _s = sp.symbols('x s', real=True)


def _build(prm):
    """주어진 파라미터로 f'(x), f(x), g(x), g'(x) 를 sympy 로 실제 계산한다."""
    a = sp.nsimplify(prm['a'])
    b = sp.nsimplify(prm['b'])
    k = sp.nsimplify(prm['k'])
    if k <= 0:
        raise ValueError('k(지수 감쇠 계수)는 양수여야 적분이 수렴한다')

    fprime = lambda var: (var - b) * sp.exp(-k * (var - b) ** 2)

    # f(x) = ∫_a^x f'(t) dt  (f(a)=0 이 자동으로 성립)
    f_x = sp.simplify(sp.integrate(fprime(_s), (_s, a, _x)))

    # 라이프니츠 규칙: g'(x) = f(x) - f(a) + a f'(x) = f(x) + a f'(x)  (f(a)=0)
    # g(x) = ∫_a^x g'(t) dt = ∫_a^x f(t) dt + a f(x)
    f_of_s = f_x.subs(_x, _s)
    g_x = sp.simplify(sp.integrate(f_of_s, (_s, a, _x)) + a * f_x)
    g_prime = sp.diff(g_x, _x)

    # (나) f(x) = g'(x) - a*f'(x) 가 모든 x 에 대해 항등식으로 성립하는지 확인
    # (이 항등식이 성립하도록 a 를 (가)의 하한/오프셋과 (나)의 계수에 동시에 썼다)
    identity_gap = sp.simplify(f_x - (g_prime - a * fprime(_x)))
    if identity_gap != 0:
        raise ValueError('조건 (가),(나)를 만족하는 f,g가 존재하지 않는다')

    return a, b, k, fprime, f_x, g_x, g_prime


def _truths(prm):
    """ㄱ, ㄴ, ㄷ 각각의 참/거짓을 sympy 계산으로 판정한다."""
    a, b, k, fprime, f_x, g_x, g_prime = _build(prm)

    # ㄱ: g'(a) 가 구조적으로 정확히 a*f'(a) 와 같은지 (문제의 <보기> ㄱ이 제시하는 수치)
    lhs_gprime_a = sp.simplify(g_prime.subs(_x, a))
    rhs_target = sp.simplify(a * fprime(a))
    stmt_1 = (sp.simplify(lhs_gprime_a - rhs_target) == 0)

    # ㄴ: f(a) = g(a)
    stmt_2 = (sp.simplify(f_x.subs(_x, a) - g_x.subs(_x, a)) == 0)

    # ㄷ: 어떤 양수 x 에 대해 g(x) < f(x), 즉 h(x)=g(x)-f(x) < 0 인 x>0 이 존재하는가
    h = sp.simplify(g_x - f_x)
    # h'(x) = f(x) 이므로 h의 극값은 f(x)=0 인 지점, 즉 |x-b|=|a-b| → x=a 또는 x=2b-a 에서 생김
    critical = sorted(set(sp.simplify(v) for v in [a, 2 * b - a] if sp.simplify(v) > 0))
    h_func = sp.lambdify(_x, h, modules=['mpmath'])

    sample_pts = list(critical)
    hi = float(max([abs(float(a)), abs(float(b)), 1.0])) * 6 + 20
    import numpy as _np
    sample_pts += list(_np.linspace(1e-4, hi, 400))

    min_h = min(float(h_func(float(xv))) for xv in sample_pts if float(xv) > 0)
    stmt_3 = bool(min_h < -1e-9)

    return stmt_1, stmt_2, stmt_3


def value(prm):
    """수학적 답: 참인 <보기> 항목들의 집합."""
    g1, g2, g3 = _truths(prm)
    labels = set()
    if g1:
        labels.add('ㄱ')
    if g2:
        labels.add('ㄴ')
    if g3:
        labels.add('ㄷ')
    return frozenset(labels)


def choices(prm):
    """5지선다 보기 목록 (이 유형의 <보기> 3개짜리 문제에서 항상 나오는 5가지 조합)."""
    return [
        frozenset({'ㄱ'}),
        frozenset({'ㄱ', 'ㄴ'}),
        frozenset({'ㄱ', 'ㄷ'}),
        frozenset({'ㄴ', 'ㄷ'}),
        frozenset({'ㄱ', 'ㄴ', 'ㄷ'}),
    ]


# 원문제의 보기 구성과 일치하는지 고정 검증
assert choices(PARAMS) == [
    frozenset({'ㄱ'}),
    frozenset({'ㄱ', 'ㄴ'}),
    frozenset({'ㄱ', 'ㄷ'}),
    frozenset({'ㄴ', 'ㄷ'}),
    frozenset({'ㄱ', 'ㄴ', 'ㄷ'}),
]


def solve(prm):
    v = value(prm)
    opts = choices(prm)
    for idx, opt in enumerate(opts, start=1):
        if opt == v:
            return idx
    raise ValueError('참인 <보기> 조합이 5지선다 중 어디에도 해당하지 않는다')


def statement(prm):
    a, b, k, fprime, f_x, g_x, g_prime = _build(prm)
    fprime_str = sp.latex((_x - b) * sp.exp(-k * (_x - b) ** 2))
    target_str = sp.latex(sp.simplify(a * fprime(a)))
    coef_str = sp.latex(a)
    a_str = sp.latex(a)
    return (
        f"함수 f(x)의 도함수가 f'(x)={fprime_str}이다. 모든 실수 x에 대하여 두 함수 f(x), g(x)가 "
        f"다음 조건을 만족시킬 때, <보기>에서 옳은 것만을 있는 대로 고른 것은?\n"
        f"(가) g(x)=\\int_{{{a_str}}}^{{x}} f'(t)(x+{a_str}-t)dt\n"
        f"(나) f(x)=g'(x)-{coef_str}f'(x)\n"
        f"<보기>\n"
        f"ㄱ. g'({a_str})={target_str}\n"
        f"ㄴ. f({a_str})=g({a_str})\n"
        f"ㄷ. 어떤 양수 x에 대하여 g(x)<f(x)이다.\n"
        f"① ㄱ  ② ㄱ,ㄴ  ③ ㄱ,ㄷ  ④ ㄴ,ㄷ  ⑤ ㄱ,ㄴ,ㄷ"
    )


if __name__ == '__main__':
    print(statement(PARAMS))
    print('value:', value(PARAMS), 'choice:', solve(PARAMS))
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
