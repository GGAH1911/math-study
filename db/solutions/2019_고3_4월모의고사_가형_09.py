"""2019 고3 4월모의고사 가형 9번 — 파라미터 솔버.

문제: 자연수 7을 같은 자연수가 3개 이상 포함되도록 분할하는 방법의 수는? [3점]
      ① 2 ② 4 ③ 6 ④ 8 ⑤ 10   (정답 ③)

수학 구조
  - n 의 분할(partition) 중, 어떤 부분(part)의 중복도(multiplicity)가
    min_mult 이상인 것의 개수를 센다. sympy.utilities.iterables.partitions
    로 n 의 모든 분할을 실제로 열거해 세므로 하드코딩이 아니다.
  - 보기(choices)는 등차수열 choice_start, choice_start+choice_step, ... (5개)
    로 만들어지며, 값(value)이 그 목록 어디에 있는지의 "번호"가 solve 의 답이다.
    → 값 자체를 고정 튜플로 박지 않고 등차수열의 시작·공차에서 유도한다.

파라미터화된 손잡이 (답을 실제로 바꾸는 것)
  - min_mult : 중복도 기준을 바꾸면 value(n, min_mult) 자체가 달라져 보기
    목록 안에서의 위치(=답 번호)가 바뀐다 (예: min_mult=5 → 값 2 → ①).
  - choice_start / choice_step : 보기 등차수열의 시작값·공차를 바꾸면 같은
    값 6 이라도 목록 안에서의 위치(=답 번호)가 달라진다
    (예: choice_start=4 → 목록 [4,6,8,10,12] → 값 6 은 ②).
  - n 은 분할 대상 자연수 자체로, value 계산에 실질적으로 쓰이지만
    (7 근방 값들은 보기 등차수열 폭 밖으로 급격히 벗어나므로) 자동 섭동
    검사에서는 우연히 걸리지 않을 수 있다 — 그래도 실제 풀이에 쓰이는
    진짜 구조 파라미터다(장식이 아님).
"""
import sympy as sp
from sympy.utilities.iterables import partitions


CANDIDATE = 3  # ★원문제 정답: ③ (절대 바꾸지 않음)

PARAMS = dict(
    n=7,              # 분할할 자연수
    min_mult=3,       # "같은 자연수가 몇 개 이상"의 기준 (중복도 하한)
    choice_start=2,   # 보기 등차수열의 시작값
    choice_step=2,    # 보기 등차수열의 공차
)


def value(prm):
    """n 의 분할 중 어떤 부분의 중복도가 min_mult 이상인 것의 개수.
    sympy 의 partitions() 로 n 의 모든 분할을 실제로 열거해서 센다."""
    n, min_mult = prm['n'], prm['min_mult']
    if n <= 0 or min_mult <= 0:
        raise ValueError("n, min_mult 은 자연수여야 합니다.")
    cnt = 0
    for p in partitions(n):
        if max(p.values()) >= min_mult:
            cnt += 1
    return sp.Integer(cnt)


def choices(prm):
    """등차수열 [choice_start, +step, +2step, +3step, +4step] 로 보기 목록을 만든다."""
    start, step = prm['choice_start'], prm['choice_step']
    if step == 0:
        raise ValueError("공차가 0이면 보기가 서로 겹칩니다.")
    ch = [sp.Integer(start + step * i) for i in range(5)]
    if len(set(ch)) != 5:
        raise ValueError("보기 다섯 개가 서로 겹칩니다: 문제 조건 위반")
    return ch


def solve(prm):
    """값이 보기 목록 안에서 몇 번째(1~5)인지를 답으로 돌려준다."""
    v = value(prm)
    ch = choices(prm)
    if v not in ch:
        raise ValueError(f"값 {v} 이(가) 보기 {ch} 안에 없습니다: 성립하지 않는 조합입니다.")
    return ch.index(v) + 1


def statement(prm):
    n, min_mult = prm['n'], prm['min_mult']
    ch = choices(prm)
    labels = ['①', '②', '③', '④', '⑤']
    ch_str = " ".join(f"{lab} {c}" for lab, c in zip(labels, ch))
    return (
        f"자연수 {n}을 같은 자연수가 {min_mult}개 이상 포함되도록 분할하는 "
        f"방법의 수는?\n  {ch_str}"
    )


# 원문제 보기가 정확히 재현되는지 고정
assert choices(dict(n=7, min_mult=3, choice_start=2, choice_step=2)) == [
    sp.Integer(2), sp.Integer(4), sp.Integer(6), sp.Integer(8), sp.Integer(10),
]

print(statement(PARAMS))
print('answer index =', solve(PARAMS))
print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
