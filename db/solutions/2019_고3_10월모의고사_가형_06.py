import sympy as sp
from sympy import symbols, simplify

CANDIDATE = 4  # 원문제 정답: ④ (값은 6)

# ----------------------------------------------------------------------------
# 문제의 수학 구조
#
#   방정식:  4^x - k*coef*2^x + N = 0     (원문제는 coef=2, 즉 k*2^(x+1) = k*coef*2^x)
#
#   t = 2^x (t > 0) 로 치환하면  t^2 - coef*k*t + N = 0.
#   두 근의 곱이 N(>0) 이므로 두 근은 항상 같은 부호이고, 방정식이 x에 대해
#   "오직 하나의 실근"을 가지려면 t>0 에서 이 이차식이 중근을 가져야 한다.
#     - 판별식 (coef*k)^2 - 4N = 0 을 k에 대해 풀어 후보를 구하고,
#       t = coef*k/2 > 0 인 branch만 채택한다 (다른 branch는 t<0 이라 기각 — 원문제의 k=-4 기각과 동일).
#   N = 4^j (= 2^(2j)) 로 두면 중근 t = 2^j 이 정확히 떨어져 alpha(=x) = j로
#   깔끔한 정수 해가 나온다. (원문제: j=2 → N=16, alpha=2)
#
#   보기는 중근 t_val 근방의 연속된 정수 다섯 개 [t_val-1 .. t_val+3] 이고,
#   구하는 값 k+alpha 가 그중 몇 번째인지가 solve()의 결과(보기 번호)다.
#
# 답을 실제로 바꾸는 파라미터(직접 실행하여 확인함):
#   - j    : 2 -> 3 이면 값이 8+3=11 로, 보기 안 위치도 4번 -> 5번으로 바뀜
#   - coef : 2 -> 4 이면 값이 2+2=4 로, 보기 안 위치도 4번 -> 2번으로 바뀜
# ----------------------------------------------------------------------------

PARAMS = dict(
    j=2,      # N = 4^j (원문제의 상수항 16 = 4^2)
    coef=2,   # k 앞의 계수 (원문제: 2^(x+1) = 2*2^x 이므로 coef=2)
)

BASE = 2  # t = 2^x 치환의 밑 (문제 형식을 유지하기 위해 고정)


def _core(prm):
    """조건을 세워 (k, alpha, 중근 t_val)을 실제로 sympy로 풀어낸다."""
    j = sp.nsimplify(prm['j'])
    coef = sp.nsimplify(prm['coef'])
    N = BASE ** (2 * j)  # 원문제의 16에 해당하는 상수항

    k = symbols('k', real=True)
    t = symbols('t', positive=True, real=True)

    eq_t = t ** 2 - coef * k * t + N
    disc = sp.discriminant(eq_t, t)  # (coef*k)^2 - 4N
    k_cands = sp.solve(sp.Eq(disc, 0), k)
    if not k_cands:
        raise ValueError('중근 조건을 만족하는 k가 존재하지 않습니다.')

    # t = coef*k/2 > 0 인 branch만 유효 (t<0인 branch는 t=2^x>0에 모순되어 기각)
    valid = []
    for kv in k_cands:
        tv = simplify(coef * kv / 2)
        if tv.is_real and tv.is_positive:
            valid.append((kv, tv))
    if len(valid) != 1:
        raise ValueError(f't>0 을 만족하는 k가 유일하지 않습니다: {valid}')
    k_val, t_val = valid[0]

    x = symbols('x', real=True)
    x_sols = [s for s in sp.solve(sp.Eq(BASE ** x, t_val), x) if s.is_real]
    if len(x_sols) != 1:
        raise ValueError(f'alpha(x)가 유일하게 정해지지 않습니다: {x_sols}')
    alpha = x_sols[0]

    # 원래 방정식에 대입해 실제로 근이 맞는지 검증
    xx, kk = symbols('x k', real=True)
    eq = BASE ** (2 * xx) - kk * coef * BASE ** xx + N
    if simplify(eq.subs([(kk, k_val), (xx, alpha)])) != 0:
        raise ValueError('원래 방정식을 만족하지 않습니다.')

    return k_val, alpha, t_val


def value(prm):
    """문제의 수학적 답: k + alpha."""
    k_val, alpha, _ = _core(prm)
    return simplify(k_val + alpha)


def choices(prm):
    """중근 t_val 근방의 연속된 정수 다섯 개로 보기를 구성한다."""
    _, _, t_val = _core(prm)
    return [simplify(t_val - 1 + i) for i in range(5)]


def solve(prm):
    """정답 보기 번호 (1~5)."""
    v = value(prm)
    ch = choices(prm)
    if v not in ch:
        raise ValueError(f'값 {v}가 보기 {ch} 범위를 벗어났습니다.')
    return ch.index(v) + 1


def statement(prm):
    j = prm['j']
    coef = prm['coef']
    N = BASE ** (2 * sp.nsimplify(j))
    ch = choices(prm)
    opts = '  '.join(f'{chr(9312 + i)} {c}' for i, c in enumerate(ch))
    if sp.nsimplify(coef) == 2:
        term = 'k \\times 2^{x+1}'
    else:
        term = f'k \\times {coef} \\times 2^{{x}}'
    return (
        f"x에 대한 방정식\n"
        f"        4^x - {term} + {N} = 0\n"
        f"이 오직 하나의 실근 \\alpha를 가질 때, k+\\alpha의 값은? "
        f"(단, k는 상수이다.)\n"
        f"{opts}"
    )


# 원문제 보기(3, 4, 5, 6, 7)와 유도된 보기, 값이 같은지 고정
assert choices(PARAMS) == [3, 4, 5, 6, 7]
assert value(PARAMS) == 6

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
