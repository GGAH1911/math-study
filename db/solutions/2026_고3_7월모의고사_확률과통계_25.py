# 1..n 카드 중 k장을 동시에 뽑을 때, 뽑은 수들의 차가 모두 d의 배수일 확률.
# 차가 d의 배수 ⇔ 뽑은 수들이 모두 같은 나머지류(mod d) 에 속함.
# 원문제: n=7, k=2, d=2 → 홀수 4장·짝수 3장 → (C(4,2)+C(3,2))/C(7,2) = 9/21 = 3/7 (보기 ①)
import sympy as sp
from itertools import combinations

CANDIDATE = 1

PARAMS = dict(
    n=7,                      # 카드에 적힌 자연수 1..n
    k=2,                      # 동시에 꺼내는 카드 장수
    d=2,                      # 차가 이 수의 배수여야 함
    choices=[sp.Rational(3, 7), sp.Rational(10, 21), sp.Rational(11, 21),
             sp.Rational(4, 7), sp.Rational(13, 21)],   # 보기 ①~⑤ 의 값
)


def probability(n, k, d):
    """1..n 에서 k장을 뽑을 때 모든 두 수의 차가 d의 배수일 확률 (기약분수)."""
    total = sp.binomial(n, k)
    if total == 0:
        return sp.Integer(0)
    # 같은 나머지류에 속한 카드끼리만 뽑아야 한다
    sizes = [len([x for x in range(1, n + 1) if x % d == r]) for r in range(d)]
    good = sum(sp.binomial(s, k) for s in sizes)
    return sp.Rational(good, total)


def brute(n, k, d):
    """작은 경우엔 전수 열거로 위 공식을 교차검증."""
    tot = list(combinations(range(1, n + 1), k))
    good = [c for c in tot if all((b - a) % d == 0 for a, b in combinations(c, 2))]
    return sp.Rational(len(good), len(tot))


def solve(prm):
    """조건 → 정답 보기 번호. 보기에 없으면 0."""
    n, k, d = prm['n'], prm['k'], prm['d']
    p = probability(n, k, d)
    if sp.binomial(n, k) <= 5000:
        assert p == brute(n, k, d), '공식과 전수열거 불일치'
    for i, c in enumerate(prm['choices'], 1):
        if sp.simplify(p - sp.Rational(c)) == 0:
            return i
    return 0


def statement(prm):
    n, k, d = prm['n'], prm['k'], prm['d']
    opts = ' '.join(f'{"①②③④⑤"[i]}{sp.latex(sp.Rational(c))}'
                    for i, c in enumerate(prm['choices']))
    return (f'주머니에 숫자 1부터 {n}까지의 자연수가 하나씩 적혀 있는 {n}장의 카드가 들어 있다. '
            f'이 주머니에서 임의로 {k}장의 카드를 동시에 꺼낼 때, 꺼낸 {k}장의 카드에 적힌 '
            f'수의 차가 모두 {d}의 배수일 확률은? [3점]\n{opts}')


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
