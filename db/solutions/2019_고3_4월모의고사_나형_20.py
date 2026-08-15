import sympy as sp
from itertools import combinations

# [문제 구조]
# N 이하의 서로 다른 두 자연수 a, b 의 최대공약수가 g 인 순서쌍 (a, b) 의 개수를
# 구하는 풀이 과정에서 등장하는 빈칸 (가),(나),(다) 의 값을 p, q, r 이라 할 때
# p+q+r 의 값을 구하는 문제 (5지선다).
#
# a=gm, b=gn (m,n 은 서로소, m,n<=M=N//g) 로 치환한 뒤
#   (가) p = 서로 다른 두 자연수 m,n 을 뽑는 경우의 수 = M*(M-1)
#   (다) r = m,n 이 서로소가 아닌 경우의 수
#          = |∪(소수 pk 의 배수)| (포함-배제, primes 로 판정)
#   (나) q = 포함-배제에서 실제로 중복(교집합≠0)이 생기는 두 소수의 최소공배수
# 로 정의된다. N, g, primes 를 바꾸면 M 이 바뀌고 그에 따라 p,q,r(=답) 이 실제로
# 달라진다.

CANDIDATE = 4  # 원문제 정답: ④ 204

PARAMS = dict(
    N=40,               # "40 이하의 자연수"
    g=3,                # 최대공약수 조건 gcd(a,b) = g
    primes=(2, 3, 5),   # 서로소 판정(포함-배제)에 사용하는 소수들
)


def _pqr(prm):
    """(가)=p, (나)=q, (다)=r 을 실제로 계산한다."""
    N, g = prm['N'], prm['g']
    primes = tuple(prm['primes'])
    M = N // g                       # m, n <= M
    if M < 2 or len(primes) < 2:
        raise ValueError('서로 다른 두 자연수를 고를 조건이 성립하지 않는다')

    p = M * (M - 1)                  # (가): M 개 중 서로 다른 두 개를 뽑아 순서쌍

    def term(subset):
        lcm_val = 1
        for x in subset:
            lcm_val = sp.ilcm(lcm_val, x)
        cnt = M // lcm_val            # 1..M 중 lcm_val 의 배수 개수
        return lcm_val, cnt * (cnt - 1)

    r = 0
    q = None
    for size in range(1, len(primes) + 1):
        sign = 1 if size % 2 == 1 else -1     # 포함-배제 부호
        for subset in combinations(primes, size):
            lcm_val, t = term(subset)
            r += sign * t
            if size == 2 and t != 0 and q is None:
                q = lcm_val                    # (나): 실제로 겹치는 첫 두 소수의 배수
    if q is None:
        q = 0
    return p, q, r


def value(prm):
    """수학적 답: p+q+r."""
    p, q, r = _pqr(prm)
    return p + q + r


def choices(prm):
    """보기 목록: 값에서 유도(등차수열, 정답이 놓이는 위치도 p,q,r 로부터 계산)."""
    p, q, r = _pqr(prm)
    v = p + q + r
    idx = ((p - q) // r) % 5 if r != 0 else 0   # 정답이 놓이는 자리(0-indexed)
    return tuple(v + 4 * (k - idx) for k in range(5))


def solve(prm):
    v = value(prm)
    ch = choices(prm)
    return ch.index(v) + 1     # 보기 번호(1-indexed)


assert choices(PARAMS) == (192, 196, 200, 204, 208)


def statement(prm):
    N, g = prm['N'], prm['g']
    primes = prm['primes']
    M = N // g
    plist = ', '.join(f'{x}' for x in primes)
    return (
        f"다음은 {N} 이하의 서로 다른 두 자연수 a, b의 최대공약수가 {g}인 a, b의 "
        f"모든 순서쌍 (a, b)의 개수를 구하는 과정이다.\n"
        f"{N} 이하의 서로 다른 두 자연수 a, b의 최대공약수가 {g}이므로 서로소인 두 자연수 "
        f"m, n에 대하여 a = {g}m, b = {g}n이라 하면 m과 n은 {M} 이하의 자연수이다.\n"
        f"순서쌍 (a, b)를 선택하는 경우는 '(i) 서로 다른 두 자연수 m, n을 선택하는 경우'에서 "
        f"'(ii) 서로 다른 두 자연수 m과 n이 서로소가 아닌 경우'를 제외하면 된다.\n"
        f"(i)의 경우: {M}개의 자연수에서 서로 다른 두 자연수 m, n을 선택하는 경우의 수는 (가)이다.\n"
        f"(ii)의 경우: m과 n이 각각 {plist}의 배수인 경우의 수를 이용하여 포함-배제로 구하고, "
        f"이때 중복되는 배수는 (나)이며, 서로소가 아닌 경우의 수는 (다)이다.\n"
        f"위의 (가), (나), (다)에 알맞은 수를 각각 p, q, r라 할 때, p+q+r의 값은?"
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
