import sympy as sp
from sympy import symbols, Eq, Rational, simplify, summation, fraction
from sympy import solve as sp_solve

# ── 문제의 수학 구조 ──────────────────────────────────────────────
# 공차 d(≠0)인 등차수열 a_n = a_1+(n-1)d 에서 조건 a_p = k·a_q 가 주어지면
#   a_1 + (p-1)d = k(a_1 + (q-1)d)  →  a_1 = d·[k(q-1)-(p-1)]/(1-k)
# 로 a_1 이 d 에 대한 비율(ratio)로 유일하게 정해진다(k≠1, p≠q).
# a_n = d(n + c)  (c = ratio - 1) 로 쓰면
#   (a_{n+1}-a_n)^2 / (a_n a_{n+1}) = 1/((n+c)(n+c+1))
# 이고 n=1..N 에 대한 합은 부분분수 망원급수로 1/(1+c) - 1/(N+1+c) 가 된다.
# 답을 실제로 바꾸는 파라미터: p, q, k (조건식 a_p=k·a_q 의 구조 → c 결정),
#   N (합의 상한). d 는 비율만 남고 소거되므로 파라미터로 두지 않는다.
#
# 보기(선택지) 구성: 원문제 보기는 정답에서 시작해 1/14씩 커지는 5개의 등차수열
# (③14, ④14, ⑤14, ⑥14, ⑦14 → 3/14,2/7,5/14,3/7,1/2). 이를
#   choices = [v + (i-pos)*step for i in range(5)]  (step = 1/denominator(v))
# 로 일반화하고, 정답이 그중 몇 번째(pos)에 오는지는 문제를 구성하는 정수들
# (p,q,k,N)에서 유도한 (p*q + k*N) % 5 로 정한다. 원문제(p=9,q=3,k=2,N=24)는
# p*q+k*N = 75 → pos=0 → 정답이 ①번에 오도록 맞춰져 있다.

CANDIDATE = 1  # 원문제 정답: 보기 ①

PARAMS = dict(p=9, q=3, k=2, N=24)


def _c(p, q, k):
    """조건 a_p = k*a_q 를 sympy 로 실제로 풀어 a_n = d(n+c) 의 c 를 구한다."""
    if p == q:
        raise ValueError('p, q 가 같으면 조건 a_p=k·a_q 가 자명해지거나 모순')
    if k == 1:
        raise ValueError('k=1이면 공차가 0이어야 하므로 "공차가 0이 아닌" 조건과 모순')
    d, a1 = symbols('d a1')
    eq = Eq(a1 + (p - 1) * d, k * (a1 + (q - 1) * d))
    sol = sp_solve(eq, a1)
    if not sol:
        raise ValueError('a_1 을 d 에 대해 유일하게 결정할 수 없음')
    ratio = simplify(sol[0] / d)
    if ratio.has(d):
        raise ValueError('a_1/d 비율이 d 에 무관하지 않음')
    return simplify(ratio - 1)


def value(prm):
    """sum_{n=1}^{N} (a_{n+1}-a_n)^2/(a_n a_{n+1}) 를 sympy 망원급수로 실제 계산."""
    p, q, k, N = prm['p'], prm['q'], prm['k'], prm['N']
    if not (isinstance(N, int) and N >= 1):
        raise ValueError('N 은 1 이상의 정수여야 함')
    c = _c(p, q, k)
    n = symbols('n', integer=True)
    for m in range(1, N + 2):          # a_1 .. a_{N+1} 이 전부 0이 아니어야 분모가 살아있다
        if simplify(m + c) == 0:
            raise ValueError('수열의 항이 0이 되어 분모가 0이 됨')
    term = 1 / ((n + c) * (n + 1 + c))
    total = summation(term, (n, 1, N))
    return simplify(total)


def choices(prm):
    """값에서 유도한 5지선다: v 를 포함하는 공차 1/denom(v) 등차수열.

    정답의 위치(pos)는 문제를 이루는 정수 p,q,k,N 에서 (p*q+k*N)%5 로 유도한다.
    """
    p, q, k, N = prm['p'], prm['q'], prm['k'], prm['N']
    v = value(prm)
    _, denom = fraction(v)
    if denom == 0:
        raise ValueError('값의 분모가 0')
    step = Rational(1, denom)
    pos = (p * q + k * N) % 5
    return tuple(simplify(v + (i - pos) * step) for i in range(5))


def solve(prm):
    v = value(prm)
    ch = choices(prm)
    for i, c in enumerate(ch, start=1):
        if simplify(v - c) == 0:
            return i
    raise ValueError('계산된 값이 보기 목록 어디에도 없음(설계상 발생 불가)')


def statement(prm):
    p, q, k, N = prm['p'], prm['q'], prm['k'], prm['N']
    return (
        f"공차가 0이 아닌 등차수열 \\{{a_n\\}}에 대하여 a_{{{p}}} = {k}a_{{{q}}}일 때,\n"
        f"  \\sum_{{n=1}}^{{{N}}}\\frac{{(a_{{n+1}}-a_{{n}})^{{2}}}}{{a_{{n}}a_{{n+1}}}}의 값은?"
    )


# 원문제 보기(①~⑤)가 정확히 3/14, 2/7, 5/14, 3/7, 1/2 로 재현되는지 고정 검증
_expected = (Rational(3, 14), Rational(2, 7), Rational(5, 14), Rational(3, 7), Rational(1, 2))
_got = choices(PARAMS)
assert all(simplify(a - b) == 0 for a, b in zip(_got, _expected)), f'보기 불일치: {_got}'

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
