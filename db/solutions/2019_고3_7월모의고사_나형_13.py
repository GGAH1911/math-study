from sympy import Rational, Abs, sqrt, erf, nsimplify, N

# ---------------------------------------------------------------------------
# 문제 구조:
#   전기차 배터리 용량 X ~ N(mu, sigma^2). P(X >= x) 를 표준정규분포표로 구하는
#   5지선다 문제. 표준화 Z=(x-mu)/sigma 가 "함께 주어지는 표의 z값들(z_options)"
#   중 가장 가까운 값에 대응되고, 그 위치(순번)가 곧 정답 번호가 된다.
#   ▶ 답을 바꾸는 파라미터
#     - mu(평균)·sigma(표준편차)·x(기준 용량): 이 값들이 Z=(x-mu)/sigma 를 결정한다.
#       Z가 달라지면 z_options 중 가장 가까운 항목(=정답 번호)이 바뀐다.
#     - z_options(표에 주어진 z값 목록·순서): 같은 Z라도 표의 구성이 달라지면
#       가장 가까운 항목의 위치(=보기 번호)가 바뀐다.
# ---------------------------------------------------------------------------

CANDIDATE = 2   # ★원문제 정답(보기 번호) — 절대 바꾸지 않는다

PARAMS = dict(
    mu=Rational(642, 10),        # 평균 64.2
    sigma=Rational(4, 10),       # 표준편차 0.4
    x=65,                        # 기준 용량(이상일 확률을 구하는 값)
    z_options=[Rational(5, 2), Rational(2), Rational(3, 2), Rational(1), Rational(1, 2)],
    # 문제와 함께 주어지는 표준정규분포표의 z값들. 순서가 그대로 보기 ①~⑤ 순서.
)


def _tail(z):
    """표준정규분포 위꼬리확률 P(Z>=z)를 sympy erf로 정확히 계산해 소수 4자리로 반올림한다."""
    z = nsimplify(z)
    p = (1 - erf(z / sqrt(2))) / 2
    return round(float(N(p)), 4)


def _z_of(prm):
    """조건에서 표준화 값 Z=(x-mu)/sigma 를 계산한다."""
    return (Rational(prm['x']) - prm['mu']) / prm['sigma']


def _nearest_index(z, z_options):
    """z에 가장 가까운 표 항목의 인덱스(0-based)를 찾는다(정확히 일치하면 그 값)."""
    diffs = [Abs(nsimplify(z) - nsimplify(zo)) for zo in z_options]
    return min(range(len(diffs)), key=lambda i: diffs[i])


def value(prm):
    """수학적으로 정확한 확률값 P(X>=x)."""
    return _tail(_z_of(prm))


def choices(prm):
    """보기 목록: 표에 주어진 z값들 각각에 대응하는 확률(값에서 유도)."""
    return [_tail(zo) for zo in prm['z_options']]


def solve(prm):
    """조건 -> 정답 보기 번호."""
    idx = _nearest_index(_z_of(prm), prm['z_options'])
    return idx + 1  # 1-based 보기 번호


# 유도한 보기가 원문제의 보기와 일치하는지 고정
assert choices(PARAMS) == [0.0062, 0.0228, 0.0668, 0.1587, 0.3085]
assert value(PARAMS) == choices(PARAMS)[CANDIDATE - 1]


def statement(prm):
    mu, sigma, x = prm['mu'], prm['sigma'], prm['x']
    labels = ['①', '②', '③', '④', '⑤']
    ch = choices(prm)
    opts_str = ' '.join(f'{lab} {c}' for lab, c in zip(labels, ch))
    return (
        f"어느 공장에서 생산하는 전기 자동차 배터리 1개의 용량은 평균이 {float(mu)}, "
        f"표준편차가 {float(sigma)}인 정규분포를 따른다고 한다. 이 공장에서 생산한 전기 자동차 "
        f"배터리 중 임의로 1개를 선택할 때, 이 배터리의 용량이 {x} 이상일 확률을 오른쪽 "
        f"표준정규분포표를 이용하여 구한 것은? (단, 전기 자동차 배터리 용량의 단위는 kWh 이다.) "
        f"{opts_str}"
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
