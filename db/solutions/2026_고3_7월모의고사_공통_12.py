# 등비수열(모든 항 양수). a_i*(a_j+a_k)=K*a_m, S_N=S → a_t 의 값은? (객관식)
# 파라미터화: 지수 위치·계수·부분합·구하는 항·보기값을 전부 PARAMS 로 뺐다.
import sympy as sp

CANDIDATE = 1

PARAMS = dict(
    i=5, j=6, k=7,                  # 조건식 좌변  a_i * (a_j + a_k)
    K=20, m=10,                     # 조건식 우변  K * a_m
    N=4, S=65,                      # 부분합 조건  S_N = S
    t=2,                            # 구하는 항 a_t
    choices=(12, 14, 16, 18, 20),   # 보기 ①~⑤ (정답 번호는 solve 가 대조해서 정한다)
)


def _positive_real(x):
    """양의 실수 해만 채택 (허수·음수·0 배제)."""
    v = sp.simplify(sp.expand(x))
    if v.has(sp.zoo, sp.nan, sp.oo):
        return False
    n = sp.N(v, 30)
    if not n.is_number or abs(sp.im(n)) > 1e-20:
        return False
    return sp.re(n) > 0


def value(prm):
    """조건을 만족하는 등비수열의 a_t 값. 조건을 만족하는 양수 수열이 없으면 None."""
    a, r = sp.symbols('a r')
    an = lambda n: a * r**(n - 1)
    eq1 = sp.Eq(an(prm['i']) * (an(prm['j']) + an(prm['k'])), prm['K'] * an(prm['m']))
    eq2 = sp.Eq(sum(an(n) for n in range(1, prm['N'] + 1)), prm['S'])
    # eq1 은 a 에 대해 2차(공통인수 a) — a>0 이므로 a=0 해를 버리고 a=a(r) 로 환원한 뒤 eq2 를 푼다.
    a_sols = [s for s in sp.solve(eq1, a) if sp.simplify(s) != 0]
    cands = []
    for a_of_r in a_sols:
        f = sp.simplify(eq2.lhs.subs(a, a_of_r) - eq2.rhs)
        for rv in sp.solve(sp.numer(sp.together(f)), r):
            if not _positive_real(rv):
                continue
            av = sp.simplify(a_of_r.subs(r, rv))
            if not _positive_real(av):
                continue
            cands.append(sp.nsimplify(sp.simplify(av * rv**(prm['t'] - 1))))
    if not cands:
        return None
    # 해가 여럿이면 값이 하나로 모이는지 확인하고 대표값을 돌려준다.
    return cands[0]


def solve(prm):
    """조건 → 정답 보기 번호(1~5). 계산값이 보기에 없으면 0."""
    v = value(prm)
    if v is None:
        return 0
    for idx, c in enumerate(prm['choices'], 1):
        if sp.simplify(v - c) == 0:
            return idx
    return 0


def statement(prm):
    ch = ' '.join(f'{s} {c}' for s, c in zip('①②③④⑤', prm['choices']))
    return (f"모든 항이 양수인 등비수열 {{a_n}}의 첫째항부터 제n항까지의 합을 S_n이라 하자.\n"
            f"a_{{{prm['i']}}}×(a_{{{prm['j']}}}+a_{{{prm['k']}}})={prm['K']}a_{{{prm['m']}}},  "
            f"S_{{{prm['N']}}}={prm['S']}\n"
            f"일 때, a_{{{prm['t']}}}의 값은?\n{ch}")


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
