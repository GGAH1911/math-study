# 등차수열 {a_n}, S_n = a_1+...+a_n.
#   b_n = c*(S_n - n*a_n)   (n 홀수)
#   b_n = (n-1)*a_n         (n 짝수)
# 빈칸 (가)=f(k), (나)=g(k), (다)=p 를 실제로 유도해 f(kf)+g(kg)+p 를 구한다.
#
# 파라미터화: 문제가 주는 수치는 b_2 의 값, 합의 상한 N, 그리고 물어보는 f/g 의 인덱스뿐이다.
#   (홀수항 계수 2 와 짝수항 (n-1) 은 구조 자체 — 바꾸면 a_1, d 가 한 조건으로
#    결정되지 않아 문제가 성립하지 않으므로 파라미터로 두지 않는다.)
CANDIDATE = 213
import sympy as sp

PARAMS = dict(
    b2=2,     # 주어진 조건 b_2 = 2
    N=20,     # \sum_{n=1}^{N} b_n 의 N (짝수)
    kf=2,     # (가)의 식 f(k) 를 k=kf 에서 평가
    kg=3,     # (나)의 식 g(k) 를 k=kg 에서 평가
)


def _derive(prm):
    """조건 → (f(k), g(k), p) 를 기호로 유도한다."""
    k, a1, d = sp.symbols('k a1 d')
    a = lambda i: a1 + (i - 1) * d                       # 등차수열 일반항
    S = lambda i: sp.expand(i * (a1 + a(i)) / 2)         # ㉠ 등차수열의 합

    # (ⅰ) n = 2k-1 (홀수): b_{2k-1} = 2(S_{2k-1} - (2k-1)a_{2k-1}) = f(k)*(a_1 - a_{2k-1})
    b_odd = sp.expand(2 * (S(2 * k - 1) - (2 * k - 1) * a(2 * k - 1)))
    f_k = sp.cancel(sp.together(b_odd / (a1 - a(2 * k - 1))))          # (가)

    # (ⅱ) n = 2k (짝수): b_{2k} = (2k-1)a_{2k}
    b_even = sp.expand((2 * k - 1) * a(2 * k))

    # 조건 b_2 = prm['b2'] → 첫째항 a_1 을 공차 d 로 표현
    a1_val = sp.solve(sp.Eq(b_even.subs(k, 1), prm['b2']), a1)[0]

    # (ⅰ)+(ⅱ): b_{2k-1} + b_{2k} = g(k)  (d 가 사라져야 문제가 성립)
    g_k = sp.simplify(sp.expand(b_odd + b_even).subs(a1, a1_val))      # (나)
    if g_k.has(d):
        raise ValueError('조건이 부족해 g(k) 가 공차에 의존한다')

    # (다): 짝수 N 을 pair 로 묶어 Σ_{k=1}^{N/2} g(k)
    pairs = int(prm['N']) // 2
    p = sp.simplify(sp.summation(g_k, (k, 1, pairs)))                  # (다)
    return k, f_k, g_k, p


def solve(prm=None):
    prm = PARAMS if prm is None else prm
    k, f_k, g_k, p = _derive(prm)
    return sp.simplify(f_k.subs(k, prm['kf']) + g_k.subs(k, prm['kg']) + p)


def statement(prm=None):
    prm = PARAMS if prm is None else prm
    k, f_k, g_k, p = _derive(prm)
    return (
        f"등차수열 {{a_n}}의 첫째항부터 제n항까지의 합을 S_n 이라 하자. "
        f"수열 {{b_n}}은 n이 홀수이면 b_n = 2(S_n - n a_n), n이 짝수이면 b_n = (n-1)a_n 이다. "
        f"b_2 = {prm['b2']} 일 때 \\sum_{{n=1}}^{{{prm['N']}}} b_n 을 구하는 과정에서 "
        f"b_{{2k-1}} = (가)×(a_1 - a_{{2k-1}}), b_{{2k-1}}+b_{{2k}} = (나), 그 총합 = (다) 이다. "
        f"(가)=f(k), (나)=g(k), (다)=p 라 할 때 f({prm['kf']})+g({prm['kg']})+p 의 값을 구하시오. "
        f"[f(k)={sp.sstr(f_k)}, g(k)={sp.sstr(g_k)}, p={p}]"
    )


print('VERIFY_PASS' if sp.simplify(solve(PARAMS) - CANDIDATE) == 0 else 'VERIFY_FAIL')
