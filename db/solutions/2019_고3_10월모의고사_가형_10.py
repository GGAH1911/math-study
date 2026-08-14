# 문제: 한 개의 주사위와 6개의 동전을 동시에 던질 때, 주사위 눈의 수와
# 동전 중 앞면이 나온 개수가 같을 확률은?
#
# 수학 구조 (파라미터화):
#   - 주사위는 1..n_sides 가 각각 균등확률 1/n_sides 로 나온다.
#   - 동전은 n_coin 개, 각 동전의 앞면 확률은 p = p_num/p_den (독립시행).
#     앞면 개수 X ~ B(n_coin, p), P(X=k) = C(n_coin,k) p^k (1-p)^(n_coin-k).
#   - 주사위 눈과 앞면 개수가 같을 확률
#       value = sum_{k=1}^{n_sides} (1/n_sides) * C(n_coin,k) * p^k * (1-p)^(n_coin-k)
#     (k 가 동전 개수를 넘으면 이항계수가 자동으로 0)
#   - 답을 실제로 바꾸는 파라미터: n_coin(동전 개수), n_sides(주사위 눈 수),
#     p_num/p_den(동전이 앞면일 확률) — 어느 것을 바꿔도 값과 정답 보기 번호가 달라진다.
#
# 보기(선택지) 생성:
#   원문제의 5개 보기(9/64, 19/128, 5/32, 21/128, 11/64)는 아래 4가지 "전형적인 계산
#   실수"에 정확히 대응한다(직접 역산으로 확인):
#     d1: 눈의 개수를 n_sides+1 로 착각해 (n_sides+1) 로 나눔
#     d2: 가장 작은 경우(k=1, 눈=1)를 빠뜨리고 k=2..n_sides 만 합산
#     d3: 동전 개수를 2개 적게(n_coin-2) 세어 계산
#     d4: 표본공간을 반으로 잘못 나누고(÷2) 큰 눈(k=n_sides-2..n_sides)만 고려
#   value 와 d1~d4 를 합쳐 오름차순 정렬한 목록이 보기이고, value 가 그중 몇 번째인지가
#   정답 보기 번호다. 이 4개는 고정 상수가 아니라 매번 n_sides,n_coin,p 로부터 다시
#   계산되므로, 파라미터가 바뀌면 보기 값뿐 아니라 정답이 몇 번째 보기인지도 바뀐다.

from sympy import Rational, binomial

CANDIDATE = 4  # ★원문제 정답: ④ 21/128 (보기 번호)

PARAMS = dict(
    n_sides=6,   # 주사위 눈의 수 (1..n_sides 균등)
    n_coin=6,    # 동전 개수
    p_num=1,     # 동전 앞면 확률의 분자
    p_den=2,     # 동전 앞면 확률의 분모  (p = p_num/p_den)
)


def _check_common(n, m, p):
    if n < 3:
        raise ValueError("주사위 눈의 수는 3 이상이어야 보기 구성이 성립합니다.")
    if m < 3:
        raise ValueError("동전 개수는 3 이상이어야 보기 구성이 성립합니다.")
    if not (0 < p < 1):
        raise ValueError("동전 앞면 확률은 0과 1 사이여야 합니다.")


def value(prm):
    """주사위 눈과 동전 앞면 수가 일치할 확률(정확한 유리수)."""
    n, m = prm['n_sides'], prm['n_coin']
    p = Rational(prm['p_num'], prm['p_den'])
    _check_common(n, m, p)
    return sum(
        Rational(1, n) * binomial(m, k) * p ** k * (1 - p) ** (m - k)
        for k in range(1, n + 1)
    )


def _distractors(prm):
    n, m = prm['n_sides'], prm['n_coin']
    p = Rational(prm['p_num'], prm['p_den'])

    # d1: 눈의 개수를 하나 많게 착각 (n -> n+1) 하여 나눔
    d1 = sum(
        Rational(1, n + 1) * binomial(m, k) * p ** k * (1 - p) ** (m - k)
        for k in range(1, n + 1)
    )
    # d2: 가장 작은 경우(k=1)를 빠뜨림
    d2 = sum(
        Rational(1, n) * binomial(m, k) * p ** k * (1 - p) ** (m - k)
        for k in range(2, n + 1)
    )
    # d3: 동전 개수를 2개 적게 셈
    mb = m - 2
    d3 = sum(
        Rational(1, n) * binomial(mb, k) * p ** k * (1 - p) ** (mb - k)
        for k in range(1, n + 1)
    )
    # d4: 표본공간을 반으로 잘못 나누고, 큰 눈(n-2..n)만 고려
    d4 = sum(
        Rational(1, 2) * binomial(m, k) * p ** k * (1 - p) ** (m - k)
        for k in range(n - 2, n + 1)
    )
    return [d1, d2, d3, d4]


def choices(prm):
    """정답과 4개의 전형적 오답을 오름차순으로 나열한 보기 목록."""
    v = value(prm)
    ds = _distractors(prm)
    opts = [v] + ds

    if any(o <= 0 for o in opts):
        raise ValueError("0 이하인 보기가 생겨 문제가 성립하지 않습니다.")
    if len(set(opts)) != len(opts):
        raise ValueError("보기 값이 겹쳐 문제가 성립하지 않습니다.")

    return sorted(opts)


def solve(prm):
    opts = choices(prm)
    v = value(prm)
    return opts.index(v) + 1  # 보기 번호(1-based)


def statement(prm):
    n, m = prm['n_sides'], prm['n_coin']
    p_num, p_den = prm['p_num'], prm['p_den']
    coin_desc = "" if (p_num, p_den) == (1, 2) else f" (단, 동전의 앞면이 나올 확률은 {p_num}/{p_den})"
    opts = choices(prm)
    circled = ['①', '②', '③', '④', '⑤']
    opt_str = "    ".join(f"{circled[i]} {o.p}/{o.q}" for i, o in enumerate(opts))
    return (
        f"한 개의 주사위(1부터 {n}까지의 눈)와 {m}개의 동전을 동시에 던질 때, "
        f"주사위를 던져서 나온 눈의 수와 {m}개의 동전 중 앞면이 나온 동전의 개수가 "
        f"같을 확률은?{coin_desc}\n  {opt_str}"
    )


# --- 원문제(6면 주사위, 동전 6개, 공정한 동전)로 보기 일치 검증 ---
_orig_choices = choices(PARAMS)
assert _orig_choices == [Rational(9, 64), Rational(19, 128), Rational(5, 32),
                          Rational(21, 128), Rational(11, 64)], _orig_choices

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
