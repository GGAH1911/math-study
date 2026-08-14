from sympy import Rational, sqrt, S

# =====================================================================
# 문제 구조
#   시민 1명의 연간 병원 이용 횟수 X ~ N(mu, sigma^2)
#   표본크기 n 인 표본평균 Xbar ~ N(mu, (sigma/sqrt(n))^2)
#   구간 [a, b] 에서 표본평균이 속할 확률 P(a<=Xbar<=b) 를
#   "표준정규분포표(0.5 간격 grid)"를 이용해 구하는 문제.
#
#   파라미터로 뽑아낸 수학 구조
#     mu, sigma, n : 모집단 정규분포 평균·표준편차, 표본크기
#     a, b         : 표본평균이 속하는 구간의 양끝값
#   -> z_low=(a-mu)/(sigma/sqrt(n)), z_high=(b-mu)/(sigma/sqrt(n))
#      가 표준정규분포표 grid(0.5, 1.0, 1.5, ...)에 정확히 맞아야
#      실제 수능형 문제(주어진 표만으로 계산)가 성립한다.
#
#   보기(선택지) 구성 원리 (수능 기출의 전형적 오답 설계를 일반화)
#     - z_low, z_high 부호가 반대(평균이 구간 안에 있음, opp 케이스):
#         정답 = T(p)+T(q)  (p=|z_low|, q=z_high)
#         오답 = 2T(p), T(p)+T(q'), T(q)+T(q'), T(q')+T(q'')
#         (q', q'' 는 grid에서 q 바로 다음, 다다음 값)
#         -> 원문제(13.7~14.2)에서 실제로 0.6826/0.7745/0.8185/0.9104/0.9710
#            을 정확히 재현함 (아래 assert로 고정)
#     - z_low, z_high 부호가 같음(구간이 평균 한쪽에 있음, same 케이스):
#         정답 = T(q)-T(p)
#         오답 = T(p)+T(q)(부호 실수), 2T(p), 2T(q), T(q')-T(p)(격자 한 칸
#         밀림 실수)
# =====================================================================

# 표준정규분포표 P(0<=Z<=z), 0.5 간격 (문제에서 항상 표로 제공되는 값)
STD_TABLE = {
    Rational(1, 2): Rational(1915, 10000),
    Rational(1): Rational(3413, 10000),
    Rational(3, 2): Rational(4332, 10000),
    Rational(2): Rational(4772, 10000),
    Rational(5, 2): Rational(4938, 10000),
    Rational(3): Rational(4987, 10000),
}
GRID = sorted(STD_TABLE.keys())


def T(z):
    """P(0<=Z<=z), z>=0 이고 grid 위에 있어야 함."""
    z = abs(z)
    if z == 0:
        return S(0)
    if z not in STD_TABLE:
        raise ValueError(f"z={z} 가 표준정규분포표 grid에 없습니다.")
    return STD_TABLE[z]


CANDIDATE = 2  # ★ 원문제 정답: 선지 ②

PARAMS = dict(
    mu=Rational(14),
    sigma=Rational(32, 10),   # 3.2
    n=256,
    a=Rational(137, 10),      # 13.7
    b=Rational(142, 10),      # 14.2
)


def _z_bounds(prm):
    sd = prm['sigma'] / sqrt(prm['n'])      # 표본평균의 표준편차
    z_low = (prm['a'] - prm['mu']) / sd
    z_high = (prm['b'] - prm['mu']) / sd
    if z_low >= z_high:
        raise ValueError("a < b (따라서 z_low < z_high) 이어야 합니다.")
    return z_low, z_high


def value(prm):
    """P(a <= Xbar <= b) 를 sympy 로 실제 계산."""
    z_low, z_high = _z_bounds(prm)
    if z_low < 0 and z_high > 0:
        prob = T(z_low) + T(z_high)
    elif z_low >= 0:
        prob = T(z_high) - T(z_low)
    else:  # 둘 다 음수
        prob = T(z_low) - T(z_high)
    return prob


def choices(prm):
    """value(prm) 에서 유도한 5지선다 보기 (오름차순)."""
    z_low, z_high = _z_bounds(prm)

    if z_low < 0 and z_high > 0:
        # 평균이 구간 내부에 있는 경우 (원문제 케이스)
        p, q = sorted([-z_low, z_high])  # p<=q: 작은 쪽부터 grid를 밟아 올라감
        iq = GRID.index(q)
        if iq + 2 >= len(GRID):
            raise ValueError("z_high 가 grid 끝쪽이라 오답 4개를 만들 수 없습니다.")
        q1, q2 = GRID[iq + 1], GRID[iq + 2]
        raw = {2 * T(p), T(p) + T(q), T(p) + T(q1), T(q) + T(q1), T(q1) + T(q2)}
    else:
        # 구간이 평균의 한쪽에만 있는 경우
        p, q = (z_low, z_high) if z_low >= 0 else (-z_high, -z_low)
        iq = GRID.index(q)
        if iq + 1 >= len(GRID):
            raise ValueError("q 가 grid 끝쪽이라 오답을 만들 수 없습니다.")
        q_next = GRID[iq + 1]  # b(또는 a)의 z를 한 칸 잘못 읽은 실수
        raw = {T(q) - T(p), T(p) + T(q), 2 * T(p), 2 * T(q), T(q_next) - T(p)}

    opts = sorted(raw)
    if len(opts) != 5:
        raise ValueError(f"보기 5개가 서로 겹칩니다: {opts}")
    return opts


def solve(prm):
    """보기 번호(1~5)를 반환."""
    v = value(prm)
    opts = choices(prm)
    return opts.index(v) + 1


def statement(prm):
    mu, sigma, n, a, b = prm['mu'], prm['sigma'], prm['n'], prm['a'], prm['b']
    opts = choices(prm)
    labels = ['①', '②', '③', '④', '⑤']
    opts_str = ' '.join(f"{lab} {float(o)}" for lab, o in zip(labels, opts))
    return (
        f"어느 도시의 시민 한 명이 1년 동안 병원을 이용한 횟수는 평균이 {mu}, "
        f"표준편차가 {float(sigma)}인 정규분포를 따른다고 한다. 이 도시의 시민 중에서 "
        f"임의추출한 {n}명의 1년 동안 병원을 이용한 횟수의 표본평균이 {float(a)} 이상이고 "
        f"{float(b)} 이하일 확률을 표준정규분포표를 이용하여 구한 것은?\n{opts_str}"
    )


# ---------------------------------------------------------------------
# 원문제 검증: 기본 PARAMS 로 만든 보기가 실제 원문제 보기와 정확히 일치해야 함
_default_choices = choices(PARAMS)
assert [float(c) for c in _default_choices] == [0.6826, 0.7745, 0.8185, 0.9104, 0.9710], _default_choices

print(statement(PARAMS))
print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')


# ---------------------------------------------------------------------
# VARIANTS: 파라미터가 서로 묶여 있어(z 값이 grid 에 정확히 맞아야 함) 자유롭게
# 하나씩만 흔들 수 없으므로, 성립하는 조합을 여러 개 제시한다.
VARIANTS = [
    PARAMS,  # 원문제: opp 케이스, p=1.0, q=1.5 -> 정답 ②
    dict(  # opp 케이스지만 p=0.5, q=1.0 -> 값은 다르지만 여전히 ②
        mu=Rational(50), sigma=Rational(6), n=576,
        a=Rational(50) - Rational(6, 24) * Rational(1, 2),
        b=Rational(50) + Rational(6, 24) * 1,
    ),
    dict(  # same-sign 케이스: 구간이 평균 위쪽에만 위치 -> 다른 선지
        mu=Rational(20), sigma=Rational(9, 2), n=81,
        a=Rational(20) + Rational(9, 2) / 9 * 1,       # z=1.0
        b=Rational(20) + Rational(9, 2) / 9 * Rational(3, 2),  # z=1.5
    ),
    dict(  # same-sign 케이스: 구간이 평균 아래쪽에만 위치 -> 또 다른 선지
        mu=Rational(30), sigma=Rational(8), n=64,
        a=Rational(30) - Rational(8, 8) * Rational(5, 2),  # z=-2.5
        b=Rational(30) - Rational(8, 8) * Rational(3, 2),  # z=-1.5
    ),
]

if __name__ == '__main__':
    results = []
    for i, prm in enumerate(VARIANTS):
        ans = solve(prm)
        results.append(ans)
        print(f"VARIANT {i}: value={float(value(prm)):.4f}, choices={[float(c) for c in choices(prm)]}, answer={ans}")
    diff_count = sum(1 for a in results if a != CANDIDATE)
    print(f"원문제와 다른 답을 낸 VARIANTS 수: {diff_count}")
    assert diff_count >= 2, "요구사항: VARIANTS 중 2개 이상은 원문제와 다른 답이어야 함"
