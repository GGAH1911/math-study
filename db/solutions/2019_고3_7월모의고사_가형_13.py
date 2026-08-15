from itertools import combinations
import sympy as sp

# ── 문제의 수학 구조 ────────────────────────────────────────────────
# 1..N 의 숫자가 하나씩 적힌 공 N개 중 K개를 동시에 꺼낸다.
# 꺼낸 숫자의 합이 "소수"이면 동전을 m1번, 아니면 m2번 던진다.
# 동전 앞면이 h번 나왔다는 조건 하에서, 합이 소수였을 조건부확률(베이즈 정리)을 구한다.
CANDIDATE = 5  # ★원문제 정답: 보기 ⑤ (원문제 값 4/7)

PARAMS = dict(
    N=4,   # 공의 개수(숫자 1..N) — 조합/소수 판정을 바꾸는 핵심 파라미터
    K=2,   # 동시에 꺼내는 공의 개수 — 역시 조합/소수 판정을 바꿈
    m1=2,  # 합이 소수일 때 던지는 동전 횟수
    m2=3,  # 합이 소수가 아닐 때 던지는 동전 횟수
    h=2,   # 관찰된 앞면 횟수
)


def value(prm):
    """조건부확률 P(합이 소수 | 앞면 h번)을 sympy Rational 로 실제 계산(베이즈 정리)."""
    N, K, m1, m2, h = prm['N'], prm['K'], prm['m1'], prm['m2'], prm['h']
    if K < 1 or K > N:
        raise ValueError('K 가 유효 범위를 벗어남')
    combos = list(combinations(range(1, N + 1), K))
    if not combos:
        raise ValueError('조합이 없음')

    prime_combos = [c for c in combos if sp.isprime(sum(c))]
    non_prime_combos = [c for c in combos if not sp.isprime(sum(c))]
    if not prime_combos or not non_prime_combos:
        # 모든 경우가 소수(또는 모두 비소수)이면 "그렇지 않으면" 분기가 없어져 문제가 성립하지 않는다.
        raise ValueError('소수/비소수 두 경우가 모두 존재해야 함')

    p_prime = sp.Rational(len(prime_combos), len(combos))
    p_non_prime = sp.Rational(len(non_prime_combos), len(combos))

    if h < 0 or h > m1 or h > m2:
        raise ValueError('h 는 0 이상이고 m1, m2 이하여야 함')

    half = sp.Rational(1, 2)
    p_h_given_prime = sp.binomial(m1, h) * half**m1
    p_h_given_non_prime = sp.binomial(m2, h) * half**m2

    p_h = p_h_given_prime * p_prime + p_h_given_non_prime * p_non_prime
    if p_h == 0:
        raise ValueError('P(앞면 h번) = 0, 조건이 불가능함')

    return (p_h_given_prime * p_prime) / p_h


def choices(prm):
    """정답과, 흔히 나올 수 있는 오답(잘못된 계산 경로)들을 값에서 유도해 보기 5개를 만든다.
    - d1 = P(소수)*P(비소수|h) : 사전확률과 여사건 조건부확률을 잘못 곱한 값
    - d2 = (P(h|소수)+P(h|비소수)) * v : 가능도 합을 정답에 잘못 곱한 값
    - d3 = 1 - v : 여사건(비소수일 조건부확률)을 정답으로 착각
    - d4 = 1/2 : "동전이니 반반"이라는 단순 착각
    - v  : 실제 정답
    원문제(N=4,K=2,m1=2,m2=3,h=2)에서 이 다섯 값은 정확히 2/7, 5/14, 3/7, 1/2, 4/7 이 된다."""
    v = value(prm)
    N, K, m1, m2, h = prm['N'], prm['K'], prm['m1'], prm['m2'], prm['h']
    combos = list(combinations(range(1, N + 1), K))
    prime_combos = [c for c in combos if sp.isprime(sum(c))]
    non_prime_combos = [c for c in combos if not sp.isprime(sum(c))]
    p_prime = sp.Rational(len(prime_combos), len(combos))
    half = sp.Rational(1, 2)
    p_h_given_prime = sp.binomial(m1, h) * half**m1
    p_h_given_non_prime = sp.binomial(m2, h) * half**m2

    one_minus_v = 1 - v
    d1 = p_prime * one_minus_v
    d2 = (p_h_given_prime + p_h_given_non_prime) * v
    d3 = one_minus_v
    d4 = half

    uniq = sorted({sp.nsimplify(x) for x in (d1, d2, d3, d4, v)})
    if len(uniq) != 5:
        raise ValueError('보기 후보 중 값이 겹쳐 5지선다가 성립하지 않음')
    return uniq


def solve(prm):
    v = value(prm)
    ch = choices(prm)
    for i, c in enumerate(ch, 1):
        if sp.simplify(c - v) == 0:
            return i
    raise ValueError('계산된 값이 보기 목록에 없음')


def statement(prm):
    N, K, m1, m2, h = prm['N'], prm['K'], prm['m1'], prm['m2'], prm['h']
    ch = choices(prm)
    marks = ['①', '②', '③', '④', '⑤']
    opts = ' '.join(f'{marks[i]} {c}' for i, c in enumerate(ch))
    return (
        f'주머니에 1부터 {N}까지의 숫자가 하나씩 적혀 있는 {N}개의 공이 들어 있다. '
        f'이 주머니에서 임의로 {K}개의 공을 동시에 꺼낼 때, 꺼낸 공에 적혀 있는 숫자의 합이 '
        f'소수이면 1개의 동전을 {m1}번 던지고, 소수가 아니면 1개의 동전을 {m2}번 던진다. '
        f'동전의 앞면이 {h}번 나왔을 때, 꺼낸 {K}개의 공에 적혀 있는 숫자의 합이 소수일 확률은?\n'
        f'{opts}'
    )


# 원문제(N=4,K=2,m1=2,m2=3,h=2)에서 유도한 보기가 원문제 보기와 정확히 일치하는지 고정
assert choices(PARAMS) == [sp.Rational(2, 7), sp.Rational(5, 14), sp.Rational(3, 7),
                            sp.Rational(1, 2), sp.Rational(4, 7)]

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
