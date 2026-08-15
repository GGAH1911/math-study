import sympy as sp
from sympy import Rational as R, S, symbols, Eq, solve as sp_solve

# ── 문제의 수학 구조 ──────────────────────────────────────────────
# "1보다 큰 두 실수 a, b 에 대하여 log_a(a^p / b^q) = c 가 성립할 때,
#  log_a b + k*log_b a 의 값은?" 형태의 로그 성질 문제.
#
# 풀이:
#   log_a(a^p / b^q) = p - q*log_a b = c  →  log_a b = (p-c)/q   (t 라 하자)
#   log_b a = 1/t (밑변환)
#   답 = t + k/t
# 원문제는 p=3, q=2, c=2, k=3 인 경우이고, 이때 t=1/2, 답=13/2 로
# 이는 다섯 보기 중 다섯째(⑤)이다.
#
# 보기(選擇肢)는 값 13/2 를 정답 자리(맨 위)에 두고, 아래 네 개는 이 유형에서
# 흔히 나오는 오답(계수를 하나 덜 센 실수 t+(k-1)/t, 전개 부호 실수 k/t-2t,
# 마지막 덧셈에서 1 또는 1/2 만큼 착오)로 구성된다 — 즉 value(prm) 하나로부터
# choices(prm) 전체가 유도된다(규칙 4).
#
# ★p, q, c, k 는 서로 묶여 있다: 보기 중 정답의 순위(몇 번째 보기인가)는
#   전적으로 t=(p-c)/q 의 부호에만 좌우되고(부호가 바뀌면 순위가 5→3위로
#   바뀜), p·q·k 를 개별적으로 +1/+2/2배 만큼만 올려서는 이 부호가 절대
#   뒤집히지 않는다(수치 실험으로 확인: p,q,k 단독 변화는 항상 답 5 유지,
#   c 만 단독으로도 부호를 뒤집을 수 있으나 그 경우 1개뿐이라 최소 개수
#   기준(2개)에 못 미친다). 따라서 규칙 5 에 따라 실제로 성립하고 답이
#   달라지는 (p,q,c,k) 조합을 VARIANTS 로 여러 개 제시한다.

CANDIDATE = 5  # ★원문제 정답 (⑤ 13/2 → 다섯 번째 보기)

PARAMS = dict(
    p=3,  # log_a(a^p / b^q) 의 p
    q=2,  # log_a(a^p / b^q) 의 q
    c=2,  # 우변 상수
    k=3,  # log_a b + k*log_b a 의 계수 k
)


def value(prm):
    """log_a(a^p/b^q)=c 를 sympy 로 실제로 풀어 log_a b 를 구하고,
    log_a b + k*log_b a 의 값을 계산한다."""
    p, q, c, k = prm['p'], prm['q'], prm['c'], prm['k']
    if q == 0:
        raise ValueError("q=0 이면 log_a b 를 유일하게 결정할 수 없다")
    t = symbols('t')  # t = log_a b
    sols = sp_solve(Eq(S(p) - S(q) * t, S(c)), t)
    if not sols:
        raise ValueError("log_a b 를 구할 수 없다")
    L = sols[0]
    if L == 0:
        raise ValueError("log_a b = 0 이면 log_b a(=1/log_a b) 가 정의되지 않는다")
    V = L + S(k) / L
    return L, V


def choices(prm):
    """value(prm)에서 유도한 5지선다 보기 — 이 유형에서 흔한 오답 패턴 포함.

    d1: 계수 k 를 하나 덜 센 실수      t + (k-1)/t
    d2: 전개 과정의 부호 실수          k/t - 2t
    d3: 마지막 덧셈에서 1 만큼 착오     V - 1
    d4: 마지막 덧셈에서 1/2 만큼 착오   V - 1/2
    정답: V
    """
    L, V = value(prm)
    k = prm['k']
    d1 = L + R(k - 1, 1) / L
    d2 = R(k, 1) / L - 2 * L
    d3 = V - 1
    d4 = V - R(1, 2)
    cands = [d1, d2, d3, d4, V]
    ordered = sorted(cands, key=lambda e: sp.nsimplify(e))
    if len(set(ordered)) != 5:
        raise ValueError("보기 값이 겹쳐 5지선다로 성립하지 않는다")
    return ordered


def solve(prm):
    """value(prm)의 값이 정렬된 보기 중 몇 번째(1-based)인지를 답으로 돌려준다."""
    L, V = value(prm)
    ch = choices(prm)
    for i, c in enumerate(ch, start=1):
        if sp.simplify(c - V) == 0:
            return i
    raise ValueError("계산한 값이 보기 목록 어디에도 없다")


def statement(prm):
    p, q, c, k = prm['p'], prm['q'], prm['c'], prm['k']
    ch = choices(prm)
    labels = ['①', '②', '③', '④', '⑤']
    opts = '  '.join(f'{lb} {sp.latex(c)}' for lb, c in zip(labels, ch))
    coeff = '' if k == 1 else f'{k} '
    return (
        "1보다 큰 두 실수 a, b에 대하여\n"
        f"  \\log_{{a}} \\frac{{a^{{{p}}}}}{{b^{{{q}}}}} = {c}\n"
        f"가 성립할 때, \\log_a b + {coeff}\\log_b a의 값은?\n"
        f"{opts}"
    )


# 원문제(p=3,q=2,c=2,k=3) 기준으로 유도한 보기가 실제 원문제 보기와 일치하는지 고정
assert choices(PARAMS) == [R(9, 2), R(5), R(11, 2), R(6), R(13, 2)]

# p,q,k 를 개별로 흔들면 정답 순위가 절대 바뀌지 않으므로(위 주석 참고),
# 실제로 성립하고 답이 달라지는 (p,q,c,k) 조합을 직접 제시한다(규칙 5).
VARIANTS = [
    dict(p=3, q=2, c=4, k=3),  # t=-1/2, V=-13/2 → ③ (원문제와 다른 답)
    dict(p=4, q=1, c=6, k=2),  # t=-2,   V=-3    → ③ (원문제와 다른 답)
    dict(p=2, q=3, c=5, k=4),  # t=-1,   V=-5    → ③ (원문제와 다른 답)
    dict(p=1, q=2, c=0, k=2),  # t=1/2,  V=9/2   → ⑤ (원문제와 같은 자리, 값은 다른 문제)
]

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
