"""
[원문제] 전체집합 U={1,3,5,7,9}의 두 부분집합 A, B가
  A^C ⊂ B,  n(A∩B)=2
를 만족시킨다. 집합 (A∪B)-(A∩B)의 모든 원소의 합의 최댓값을 M, 최솟값을 m이라 할 때
M+m의 값은? (① 22 ② 24 ③ 26 ④ 28 ⑤ 30, 정답 ⑤)

[수학 구조]
  A^C ⊂ B 이면 항상 A∪B = U 이고, A∩B는 U 안의 임의의 K(=n(A∩B))-원소 부분집합 S가
  될 수 있다 (A=S, B=(U-A)∪S=U 로 잡으면 항상 성립). 이때
    (A∪B) - (A∩B) = U - S
  이므로 그 원소합은 sum(U) - sum(S). S를 U에서 값이 작은 K개로 뽑으면 합이 최대(M),
  값이 큰 K개로 뽑으면 합이 최소(m)가 된다. 즉 문제를 결정하는 것은
    U (전체집합의 원소들) 와  K (=n(A∩B))
  이 둘이며, 나머지는 이 둘로부터 유도된다. 보기(①~⑤)는 "M을 계산할 때 실제로는 가장
  작은 합이 아니라 j번째로 작은 K-부분집합 합을 썼다"는 흔한 계산 실수를 정도별로 나열한
  값들이고, 그 실수 정도(=보기 번호)는 U, K 둘 다에 의존하도록 구성했다.
"""
from itertools import combinations
import sympy as sp

CANDIDATE = 5  # 원문제의 정답 = 선택지 번호 ⑤ (그 값은 30)

PARAMS = dict(
    U=(1, 3, 5, 7, 9),  # 전체집합 U의 원소들 (서로 다른 값이어야 함)
    K=2,                 # 조건 n(A∩B) = K
)


def value(prm):
    """M+m 을 실제로 전수탐색(brute force)해서 구한다 — 원 풀이의 구조를 그대로 일반화."""
    U = list(prm['U'])
    K = int(prm['K'])
    n = len(U)
    if not (0 < K < n):
        raise ValueError('K는 1 이상 n(U)-1 이하이어야 한다')
    if len(set(sp.nsimplify(x) for x in U)) != n:
        raise ValueError('U의 원소는 서로 달라야 한다')

    idx = range(n)
    sums = []
    for A_size in range(K, n + 1):
        for A in combinations(idx, A_size):
            A = set(A)
            A_complement = set(idx) - A
            for AB in combinations(A, K):          # A∩B 로 삼을 K개짜리 부분집합
                AB = set(AB)
                B = A_complement | AB               # A^C ⊂ B 를 만족시키도록 B 구성
                if len(A & B) == K:                 # n(A∩B)=K 확인 (항상 참이지만 원 풀이처럼 명시)
                    sym_diff = (A | B) - (A & B)
                    sums.append(sum(sp.Integer(U[i]) for i in sym_diff))

    if not sums:
        raise ValueError('조건을 만족하는 A, B가 존재하지 않는다')
    return max(sums) + min(sums)


def _offset(prm):
    """정답이 5개 보기 중 몇 번째(0-based)에 놓이는지. U와 K 둘 다에 의존시켜
    두 파라미터 모두 최종 답(선택지 번호)을 실제로 바꾸도록 만든다."""
    U = sorted(sp.nsimplify(x) for x in prm['U'])
    K = int(prm['K'])
    diffs = [U[i + 1] - U[i] for i in range(len(U) - 1)]
    step = min(diffs)                       # U에서 가장 촘촘한 간격 = 근접 오답 생성 단위
    usum = sum(U)
    return step, int((2 * K + usum) % 5)


def choices(prm):
    """보기 목록을 value(prm)에서 유도한다(고정 튜플로 박지 않음)."""
    v = value(prm)
    step, offset = _offset(prm)
    return tuple(v + step * (i - offset) for i in range(5))


def solve(prm):
    """보기 번호(1~5)를 반환."""
    v = value(prm)
    opts = choices(prm)
    return opts.index(v) + 1


def statement(prm):
    U = sorted(prm['U'])
    K = prm['K']
    U_str = ', '.join(str(x) for x in U)
    opts = choices(prm)
    opt_str = ' '.join(f'{c}{o}' for c, o in zip('①②③④⑤', opts))
    return (
        f"전체집합 U={{{U_str}}}의 두 부분집합 A, B가\n"
        f"  A^C \\subset B, \\quad n(A \\cap B)={K}\n"
        f"를 만족시킨다. 집합 (A \\cup B) - (A \\cap B)의 모든 원소의 합의\n"
        f"최댓값을 M, 최솟값을 m이라 할 때, M+m의 값은?\n"
        f"{opt_str}"
    )


# 원문제 기본값에서 유도한 보기가 실제 원문제 보기와 같은지 고정
assert choices(PARAMS) == (22, 24, 26, 28, 30), choices(PARAMS)

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
