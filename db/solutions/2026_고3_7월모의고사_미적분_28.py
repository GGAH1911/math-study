# 2026 고3 7월 모의고사 미적분 28 — 파라미터화 솔버
#
# [문제 구조]
#   f(x) = A*x - B/(e^x + C)          (A,B,C > 0 이면 f 는 순증가 → 역함수 존재)
#   x>0 에서 연속인 g 가 모든 실수 x 에 대하여
#       ∫_1^{e^x} f^{-1}(g(t)) dt = (a*x + b)*e^x + k      (k 는 상수)
#   를 만족시킬 때,  ∫_{f(p)}^{f(k)} ( f^{-1}(x) + g^{-1}(x) ) dx 의 값.
#
# [수학]
#   1) 양변을 x 로 미분:  f^{-1}(g(e^x))·e^x = (a*x + a + b)·e^x
#         ⟹ f^{-1}(g(e^x)) = a*x + a + b
#         ⟹ t = e^x 로 두면  f^{-1}(g(t)) = a·ln t + a + b,  즉 g(t) = f(a·ln t + a + b)
#   2) x = 0 대입: 좌변 = 0 이므로  0 = b + k  ⟹  k = -b      (원문제: b=-1 → k=1)
#   3) g(x) = f(a·ln x + a + b) 이므로  g^{-1}(y) = exp( (f^{-1}(y) - a - b)/a )
#   4) x = f(u) 치환(dx = f'(u)du, u: p → k):
#         ∫_{f(p)}^{f(k)} (f^{-1}(x) + g^{-1}(x)) dx
#           = ∫_p^k ( u + exp((u - a - b)/a) ) · f'(u) du
#      원문제(A=B=C=1, a=1, b=-1, p=0)에서 이 값은 정확히 e → 보기 ① .
#
# 파라미터를 바꾸면 4)의 적분이 그대로 새 문제의 답이 된다(유사문제 재생성).

import sympy as sp
from mpmath import mp, mpf, quad, exp as mexp

mp.dps = 40

CANDIDATE = 1

PARAMS = dict(
    A=1,   # f(x) = A*x - B/(e^x + C)  의 일차항 계수
    B=1,   # 분자
    C=1,   # 분모 상수
    a=1,   # 적분방정식 우변 (a*x + b)*e^x + k 의 x 계수
    b=-1,  # 적분방정식 우변의 상수항 (k = -b 가 유도된다)
    p=0,   # 적분 아래끝 f(p) 의 p
    choices=['E', '3*E/2', '2*E', '5*E/2', '3*E'],   # 보기 ①~⑤ (정답 번호는 solve 가 정한다)
)

_u = sp.Symbol('u', real=True)


def f_expr(prm):
    """f(x) = A*x - B/(e^x + C)"""
    A, B, C = sp.sympify(prm['A']), sp.sympify(prm['B']), sp.sympify(prm['C'])
    return A * _u - B / (sp.exp(_u) + C)


def k_const(prm):
    """적분방정식에 x=0 을 넣으면 좌변이 0 이므로 k = -b."""
    return sp.sympify(prm['b']) * -1


def value(prm):
    """∫_{f(p)}^{f(k)} (f^{-1}(x)+g^{-1}(x)) dx  를 치환적분으로 계산한 실제 값."""
    a, b = sp.sympify(prm['a']), sp.sympify(prm['b'])
    if a == 0:
        raise ValueError('a=0 이면 f^{-1}(g(t)) 가 t 에 의존하지 않아 g 의 역함수가 없다')
    A, B, C = sp.sympify(prm['A']), sp.sympify(prm['B']), sp.sympify(prm['C'])
    if A <= 0 or B <= 0 or C <= 0:
        raise ValueError('A,B,C > 0 이어야 f 가 순증가(역함수 존재)')
    p, k = sp.sympify(prm['p']), k_const(prm)

    fp = sp.diff(f_expr(prm), _u)            # f'(u) = A + B*e^u/(e^u+C)^2
    integrand = (_u + sp.exp((_u - a - b) / a)) * fp
    fn = sp.lambdify(_u, integrand, modules='mpmath')
    return quad(fn, [mpf(float(p)), mpf(float(k))])


def solve(prm):
    """조건 → 답. 보기에 있으면 보기 번호를, 없으면(변형문제) 값 자체를 돌려준다."""
    V = value(prm)
    for i, c in enumerate(prm['choices']):
        cv = mpf(str(sp.sympify(c).evalf(mp.dps)))
        if abs(V - cv) < mpf('1e-20') + abs(cv) * mpf('1e-25'):
            return i + 1
    return sp.Float(str(V), 25)


def statement(prm):
    """같은 유형의 새 문제 문장(보기는 계산된 답을 포함하도록 다시 만든다)."""
    A, B, C = prm['A'], prm['B'], prm['C']
    a, b = prm['a'], prm['b']
    p, k = prm['p'], k_const(prm)
    V = sp.Float(str(value(prm)), 20)
    opts = [V * sp.Rational(m, 2) for m in (2, 3, 4, 5, 6)]   # 정답을 ①에 두고 등차로 배치
    lin = (f'{a}x' if a != 1 else 'x') + (f'{b:+}' if b else '')
    txt = (f"함수 f(x)={A}x-\\frac{{{B}}}{{e^{{x}}+{C}}} 의 역함수 f^{{-1}}(x)와 "
           f"x>0에서 정의된 연속함수 g(x)가 모든 실수 x에 대하여 "
           f"\\int_{{1}}^{{e^{{x}}}}f^{{-1}}(g(t))dt=({lin})e^{{x}}+k (k는 상수) 를 만족시킨다. "
           f"함수 g(x)의 역함수 g^{{-1}}(x)에 대하여 "
           f"\\int_{{f({p})}}^{{f(k)}}(f^{{-1}}(x)+g^{{-1}}(x))dx 의 값은?")
    return {'text': txt, 'k': k, 'value': V,
            'choices': [str(o) for o in opts], 'answer_no': 1}


if __name__ == '__main__':
    v = value(PARAMS)
    print(f'k = {k_const(PARAMS)}')
    print(f'적분값 = {v}   (e = {mexp(1)})')
    print(f'답 = 보기 {solve(PARAMS)}번')
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
