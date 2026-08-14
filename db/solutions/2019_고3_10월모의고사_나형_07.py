# -*- coding: utf-8 -*-
"""
원문제: 같은 종류의 공 6개를 서로 다른 3개의 상자에, 각 상자에 1개 이상씩 넣는 경우의 수.
  정답: C(6-3+3-1, 3-1) = C(5,2) = 10  ->  보기 ⑤ (정답 번호 5)

수학 구조 (중복조합 / 별과 막대):
  x_1 + ... + x_k = n,  x_i >= lo  인 정수해의 개수.
  y_i = x_i - lo 로 치환하면 y_1 + ... + y_k = n - lo*k,  y_i >= 0 이므로
  답 = C((n - lo*k) + k - 1, k - 1)   (sympy binomial 로 실제 계산)

파라미터로 뽑은 값 (세 개 모두 답을 바꾼다):
  n  : 공의 총 개수            (원문제 6)
  k  : 서로 다른 상자의 개수    (원문제 3)
  lo : 상자마다 최소 공 개수    (원문제 1)

객관식 보기는 정답 v 를 포함하는 연속 5개 정수로 값에서 유도한다(고정 튜플 금지).
단, 보기 창을 항상 [v-4, ..., v] 로 두면 정답 위치가 언제나 ⑤가 되어
계수를 바꿔도 보기 번호(답)가 안 움직인다. 그래서 보기 창의 위치를
정답 v 의 홀짝에서 결정한다:
  v 짝수 -> [v-4, v-3, v-2, v-1, v]   (정답 = 마지막, 원문제 보기와 일치)
  v 홀수 -> [v, v+1, v+2, v+3, v+4]   (정답 = 처음)
원문제(v=10, 짝수) 보기가 [6,7,8,9,10] 임을 assert 로 고정한다.
"""
import sympy as sp

#: 원문제의 정답 — 보기 번호 ⑤ (절대 바꾸지 않는다)
CANDIDATE = 5

PARAMS = dict(
    n=6,   # 공의 총 개수
    k=3,   # 서로 다른 상자의 개수
    lo=1,  # 상자마다 최소로 넣어야 하는 공의 개수
)

#: 성립하는 다른 파라미터 조합. 셋 다 예외 없이 풀리고 원문제(답 5)와 다른 답을 낸다.
VARIANTS = [
    dict(n=7, k=3, lo=1),  # v = C(6,2) = 15 (홀수) -> 보기 번호 1
    dict(n=8, k=4, lo=1),  # v = C(7,3) = 35 (홀수) -> 보기 번호 1
    dict(n=6, k=3, lo=2),  # v = C(2,2) = 1  (홀수) -> 보기 번호 1
]


def value(prm):
    """수학적 답: C(n - lo*k + k - 1, k - 1) 를 sympy 로 계산"""
    n, k, lo = prm['n'], prm['k'], prm['lo']
    if n < 1 or k < 1:
        raise ValueError("n, k 는 1 이상이어야 한다")
    m = n - lo * k                      # 치환 후 남는 공의 개수 (음이 아닌 정수여야 성립)
    if m < 0:
        raise ValueError(f"성립 불가: 공 {n}개를 상자 {k}개에 최소 {lo}개씩 넣을 수 없다")
    return sp.binomial(m + k - 1, k - 1)


def choices(prm):
    """보기 목록: 정답 v 를 포함하는 연속 5개 정수 (값에서 유도)"""
    v = int(value(prm))
    if v % 2 == 0:                      # 짝수: 정답을 마지막(⑤)에 배치
        return list(range(v - 4, v + 1))
    return list(range(v, v + 5))        # 홀수: 정답을 처음(①)에 배치


def solve(prm):
    """조건 -> 답: 보기 번호(1~5)"""
    v = int(value(prm))
    return choices(prm).index(v) + 1


def statement(prm):
    """해당 파라미터로 만들어지는 문제 문장(한국어)"""
    opts = '  '.join(f'{mark} {c}' for mark, c in zip('①②③④⑤', choices(prm)))
    return (f"같은 종류의 공 {prm['n']}개를 남김없이 서로 다른 {prm['k']}개의 상자에 "
            f"나누어 넣으려고 한다. 각 상자에 공이 {prm['lo']}개 이상씩 들어가도록 "
            f"나누어 넣는 경우의 수는? [3점]\n  {opts}")


# --- 원문제 재현 고정 (assert) ---
assert choices(PARAMS) == [6, 7, 8, 9, 10], "유도 보기가 원문제 보기(①6 ②7 ③8 ④9 ⑤10)와 다름"
assert solve(PARAMS) == CANDIDATE == 5, "원문제 정답(⑤) 재현 실패"

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
