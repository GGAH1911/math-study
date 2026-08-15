"""
[원문제] 8개 레인(1~8) 중 서로 다른 레인을 3명의 학생이 각각 1개씩 선택할 때,
선택한 세 번호 중 어느 두 번호도 연속되지 않도록 뽑는 경우의 수.

[수학 구조]
  - n개(레인 총 개수) 중 서로 인접하지 않는 k개(학생 수)의 번호를 뽑는
    '순서 없는' 조합의 수는 C(n-k+1, k) (인접 금지 조건을 b_i = a_i-(i-1)
    로 치환하면, 서로 다른 k개를 n-k+1개 중에서 고르는 문제로 환원된다).
  - 학생은 서로 구분되므로(3명이 각자 레인을 고름) 뽑힌 k개의 번호를
    학생들에게 배정하는 순열 k! 을 곱한다.
  - 정답 값(value) = C(n-k+1, k) * k!

  [선택지 유도]
  - 이 문제의 보기 ①~⑤(120,132,144,156,168)는 정답을 중심으로
    step = 2*k! 간격으로 나열된 5개 값이다.
  - 정답이 보기 중 몇 번째에 오는지(idx0)는 원문제(n=8,k=3)에서는
    가장 작은 값(①, index 0)이었다. 이를 n,k 에 의존하는 결정적 규칙
    idx0 = (n-k-5) mod 5 로 재현한다(n=8,k=3일 때 정확히 0이 되도록
    맞춘 식) — 즉 "정답을 기준으로 몇 개의 작은 오답/큰 오답을 배치할지"를
    파라미터에 따라 순환시키는 방식으로, 원문제를 정확히 재현하면서도
    n,k가 바뀌면 정답의 보기 번호 자체도 달라지게 만든다.

파라미터로 뽑은 것:
  n : 레인(자리) 총 개수
  k : 선택하는 학생(번호) 수
  둘 다 정답 값과 정답이 위치하는 보기 번호를 모두 바꾸는 살아있는
  파라미터다.
"""
from itertools import permutations
import sympy as sp

CANDIDATE = 1  # ★보기 번호 — 원문제 정답(①) 그대로 유지

PARAMS = dict(
    n=8,  # 레인 총 개수
    k=3,  # 선택하는 학생(번호) 수
)


def value(prm):
    """어느 두 번호도 연속되지 않게 n개 중 k개를 순서를 구분해 뽑는 경우의 수."""
    n, k = prm['n'], prm['k']
    if not (isinstance(n, int) and isinstance(k, int)) or n <= 0 or k <= 0:
        raise ValueError('n, k 는 양의 정수여야 한다')
    if k > n:
        raise ValueError('k 가 n 보다 클 수 없다')
    if n - k + 1 < k:
        raise ValueError('인접하지 않게 뽑을 수 있는 조합이 존재하지 않는다')
    # 인접 금지 조합의 수: 오름차순 a_1<...<a_k, a_{i+1}-a_i>=2 를
    # b_i = a_i - (i-1) 로 치환하면 b_1<...<b_k 는 {1,...,n-k+1} 에서
    # 겹치지 않게 고르는 순수 조합 문제가 된다.
    unordered = sp.binomial(n - k + 1, k)
    # 학생(번호)이 서로 구분되므로 뽑힌 k개를 학생들에게 배정하는 순열을 곱한다
    return sp.Integer(unordered * sp.factorial(k))


CHOICES = [120, 132, 144, 156, 168]  # 원문제 보기 ①~⑤


def choices(prm):
    """value(prm) 를 포함하는 5개 보기를, step=2*k! 간격으로 생성.

    정답이 몇 번째 자리(idx0)에 오는지는 (n-k-5) mod 5 로 결정한다.
    n=8,k=3 일 때 idx0=0 이 되어 원문제와 정확히 일치한다.
    """
    n, k = prm['n'], prm['k']
    v = int(value(prm))
    step = 2 * int(sp.factorial(k))
    idx0 = (n - k - 5) % 5
    return [v + step * (i - idx0) for i in range(5)]


def solve(prm):
    """보기 중 정답의 번호(1-indexed)를 반환."""
    v = int(value(prm))
    opts = choices(prm)
    return opts.index(v) + 1


# 원문제 파라미터에서 유도된 보기가 실제 원문제 보기와 일치하는지 고정
assert choices(PARAMS) == CHOICES


def statement(prm):
    n, k = prm['n'], prm['k']
    opts = choices(prm)
    labels = ['①', '②', '③', '④', '⑤']
    opt_str = '  '.join(f'{lab} {o}' for lab, o in zip(labels, opts))
    return (
        f"어느 수영장에 1번부터 {n}번까지 {n}개의 레인이 있다.\n"
        f"  {k}명의 학생이 서로 다른 레인의 번호를 각각 1개씩 선택할 때,\n"
        f"  {k}명의 학생이 선택한 레인의 {k}개 번호 중 어느 두 번호도\n"
        f"  연속되지 않도록 선택하는 경우의 수는? [4점]\n\n"
        f"  {opt_str}"
    )


def _brute_force_check(n, k):
    """작은 n,k 에 대해 완전탐색으로 공식을 검증(개발 확인용, solve 경로에는 없음)."""
    count = 0
    for combo in permutations(range(1, n + 1), k):
        if all(abs(combo[i] - combo[j]) >= 2 for i in range(k) for j in range(i + 1, k)):
            count += 1
    return count


if __name__ == '__main__':
    # 개발 확인: 원문제 파라미터에서 완전탐색과 공식이 일치하는지 검사
    assert _brute_force_check(PARAMS['n'], PARAMS['k']) == int(value(PARAMS))
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
