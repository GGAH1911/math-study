"""
2019 고3 10월모의고사 가형 15번
주머니에 1~N 의 자연수가 하나씩 적힌 N개의 공이 있다. 이 중 K개를 임의로 동시에
꺼내 오름차순으로 나열했을 때 가장 작은 수를 a 라 하자. 뽑힌 K개의 합이 짝수일 때,
a가 홀수일 조건부확률을 구하는 문제.

★파라미터화한 수학 구조
  - N : 주머니 속 자연수의 최댓값 (원문제 8)
  - K : 동시에 꺼내는 공의 개수 (원문제 3, a<b<c 라 명명된 것이 곧 K=3인 경우)
  N, K 를 바꾸면 표본공간 C(N,K)·짝수합 부분집합·그중 최솟값이 홀수인 부분집합의
  크기가 모두 달라져 조건부확률 값 자체가 달라진다 → 답을 바꾸는 파라미터가 2개.

★선택지 재현 구조
  원문제 선택지 3/7, 1/2, 4/7, 9/14, 5/7 을 14를 공통분모로 보면
  6/14, 7/14, 8/14, 9/14, 10/14 로 "분자가 1씩 증가하는 5개의 연속 정수" 이고
  정답(5/7=10/14)이 그중 맨 끝(⑤)에 위치한다.
  이를 일반화해, 정답 값 v=p/q(기약분수)를 D=2q 위에서 분자 n=2p 로 표현하고,
  n을 포함하는 길이 5의 연속정수 구간 [n-offset, n-offset+4] 를 선택지로 삼는다.
  구간에서 n이 놓이는 위치(offset)는 offset=(N*K) mod 5 로 정하며, 원문제
  (N,K)=(8,3) 일 때 offset=4, 즉 정답이 맨 끝(⑤)에 오도록 맞춰져 있어 원문제 배치와
  정확히 일치한다.
"""
from itertools import combinations
import sympy as sp

CANDIDATE = 5   # ★절대 바꾸지 마세요 (원문제 정답: 선택지 ⑤)

PARAMS = dict(
    N=8,   # 주머니 속 자연수 1..N
    K=3,   # 동시에 꺼내는 공의 개수 (a = 뽑힌 수 중 최솟값)
)


def value(prm):
    """조건부확률 P(최솟값이 홀수 | 합이 짝수) 를 실제로 계산한다 (수학적 답)."""
    N, K = prm['N'], prm['K']
    if K < 1 or K > N:
        raise ValueError('K는 1 이상 N 이하이어야 한다')
    nums = list(range(1, N + 1))
    combos = list(combinations(nums, K))
    even_sum = [c for c in combos if sum(c) % 2 == 0]
    if not even_sum:
        raise ValueError('합이 짝수인 경우의 수가 없음 — 조건부확률 정의 불가')
    a_odd = [c for c in even_sum if min(c) % 2 == 1]
    return sp.Rational(len(a_odd), len(even_sum))


def choices(prm):
    """value(prm) 에서 유도한 5개의 보기(값에서 결정되며 임의 상수를 박지 않는다)."""
    N, K = prm['N'], prm['K']
    v = value(prm)
    p, q = sp.fraction(v)
    D = 2 * q                    # 원문제의 공통분모 14 = 2*7 을 일반화
    n = 2 * p                    # 그 분모 위에서 정답의 분자
    offset = (N * K) % 5         # 정답이 5개 구간 중 몇 번째(0..4)에 놓이는지
    nums = [n - offset + i for i in range(5)]
    return [sp.Rational(x, D) for x in nums]


# 원문제 선택지 재현 검증: ① 3/7 ② 1/2 ③ 4/7 ④ 9/14 ⑤ 5/7
assert choices(dict(N=8, K=3)) == [
    sp.Rational(3, 7), sp.Rational(1, 2), sp.Rational(4, 7),
    sp.Rational(9, 14), sp.Rational(5, 7),
]


def solve(prm):
    """조건 → 보기 번호."""
    ch = choices(prm)
    v = value(prm)
    return ch.index(v) + 1   # 1-indexed 선택지 번호


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
