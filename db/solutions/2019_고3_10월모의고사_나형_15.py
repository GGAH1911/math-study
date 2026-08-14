from collections import Counter
from sympy import Rational, binomial

# ------------------------------------------------------------------
# 문제 구조
#   A, B, C 가 각각 주사위를 n번씩 던져 "1의 눈"이 나온 횟수로 승자를 정한다.
#     (가) 세 사람의 횟수가 모두 다르면 -> 가장 많이 나온 사람이 승자
#     (나) 두 사람만 횟수가 같으면    -> 나머지(다른) 한 사람이 승자
#     (다) 세 사람의 횟수가 모두 같으면 -> 모두 승자
#   A는 이미 n번을 다 던져 1이 a번, B도 n번을 다 던져 1이 b번 나왔다.
#   C는 k번째 던지기에서 "처음으로" 1이 나왔다(그 전 k-1번은 1이 아님) ->
#   현재 C의 1의 개수는 1, 남은 던지기 횟수는 n-k 번.
#   남은 n-k 번 중 1이 나오는 횟수 X ~ Binomial(n-k, 1/m) (m면체 주사위, 그중 1은 눈금 1개)
#   최종 C의 개수 c = 1 + X 이고, 목표 인물 targets(예: A 또는 C)가 승자가 될 확률을 구한다.
# ------------------------------------------------------------------

CANDIDATE = Rational(13, 18)  # 원문제 정답: "A 또는 C가 승자가 될 확률" = 13/18 (보기 ②)  ★절대 바꾸지 마세요

PARAMS = dict(
    n=5,             # 각자 주사위를 던지는 횟수
    a=2,             # A의 1의 눈 나온 횟수 (n번 다 던진 확정값)
    b=1,             # B의 1의 눈 나온 횟수 (n번 다 던진 확정값)
    k=3,             # C가 k번째 던지기에서 처음으로 1이 나옴 (그 전엔 전부 1이 아님)
    m=6,             # 주사위 눈의 수 (1이 나올 확률 = 1/m)
    targets=('A', 'C'),  # "A 또는 C가 승자" 에서 묻는 대상
)


def determine_winners(a, b, c):
    """세 사람의 1의 눈 횟수 (a, b, c) 로부터 규칙 (가)(나)(다) 에 따라 승자 집합을 구한다."""
    counts = {'A': a, 'B': b, 'C': c}
    distinct = set(counts.values())
    if len(distinct) == 1:
        return set(counts)  # (다) 모두 같으면 전원 승자
    if len(distinct) == 3:
        mx = max(counts.values())
        return {p for p, v in counts.items() if v == mx}  # (가) 최다인 사람
    cnt = Counter(counts.values())
    lone_val = next(v for v, c2 in cnt.items() if c2 == 1)
    return {p for p, v in counts.items() if v == lone_val}  # (나) 혼자 다른 사람


def value(prm):
    """조건을 만족하는 확률(수학적 답)을 sympy 로 실제 계산."""
    n, a, b, k, m = prm['n'], prm['a'], prm['b'], prm['k'], prm['m']
    targets = set(prm.get('targets', ('A', 'C')))

    if not (isinstance(n, int) and n >= 1):
        raise ValueError("n은 1 이상의 정수여야 합니다.")
    if not (0 <= a <= n and 0 <= b <= n):
        raise ValueError("a, b는 0 이상 n 이하여야 합니다.")
    if not (1 <= k <= n):
        raise ValueError("k(첫 1이 나온 순번)는 1 이상 n 이하여야 합니다.")
    if not (isinstance(m, int) and m >= 2):
        raise ValueError("m(주사위 눈의 수)은 2 이상의 정수여야 합니다.")
    if not targets <= {'A', 'B', 'C'}:
        raise ValueError("targets는 A, B, C 중에서만 골라야 합니다.")

    remaining = n - k      # C가 아직 던지지 않은 횟수
    base_c = 1              # k번째에 처음 1이 나왔으므로 현재까지 C의 1의 개수 = 1
    p1 = Rational(1, m)
    p0 = 1 - p1

    total = Rational(0)
    for x in range(remaining + 1):
        c = base_c + x
        prob_x = binomial(remaining, x) * p1 ** x * p0 ** (remaining - x)
        winners = determine_winners(a, b, c)
        if winners & targets:
            total += prob_x
    return total


def choices(prm):
    """value(prm) 을 중심으로 원문제와 동일한 방식(공통분모 기준 인접 정수 오프셋)의 5지선다 보기를 유도."""
    v = Rational(value(prm))
    D = v.q
    N = v.p
    return tuple(Rational(N + off, D) for off in (-1, 0, 1, 2, 3))


def solve(prm):
    return value(prm)


def statement(prm):
    n, a, b, k, m = prm['n'], prm['a'], prm['b'], prm['k'], prm['m']
    targets = prm.get('targets', ('A', 'C'))
    dice = "주사위" if m == 6 else f"1부터 {m}까지의 눈이 하나씩 있는 주사위"
    tgt = " 또는 ".join(targets)
    return (
        f"A, B, C 세 사람이 한 개의 {dice}를 각각 {n}번씩 던진 후 다음 규칙에 따라 승자를 정한다.\n"
        f"(가) 1의 눈이 나온 횟수가 세 사람 모두 다르면, 1의 눈이 가장 많이 나온 사람이 승자가 된다.\n"
        f"(나) 1의 눈이 나온 횟수가 두 사람만 같다면, 횟수가 다른 나머지 한 사람이 승자가 된다.\n"
        f"(다) 1의 눈이 나온 횟수가 세 사람 모두 같다면, 모두 승자가 된다.\n"
        f"A와 B가 각각 주사위를 {n}번씩 던진 후, A는 1의 눈이 {a}번, B는 1의 눈이 {b}번 나왔다. "
        f"C가 주사위를 {k}번째 던졌을 때 처음으로 1의 눈이 나왔다. {tgt}가 승자가 될 확률은?"
    )


# 원문제 보기(①~⑤)와 정확히 일치하는지, 정답이 보기 ②에 위치하는지 고정
_base_choices = choices(PARAMS)
assert _base_choices == (Rational(2, 3), Rational(13, 18), Rational(7, 9), Rational(5, 6), Rational(8, 9))
assert _base_choices[1] == CANDIDATE

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
