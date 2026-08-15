"""
[확률과 통계] 2x2 분할표 조건부확률 문제의 파라미터화 솔버.

원문제: 학생들을 "영화 관람 희망 여부(열)" × "뮤지컬 관람 희망 여부(행)"로 분류한
2x2 분할표가 주어지고, "영화 관람을 희망한 학생 중 뮤지컬 관람도 희망한 학생일 확률"
(조건부확률)을 구하는 5지선다 문제.

파라미터로 뽑은 수학 구조
------------------------
  p11 = 영화 희망 ∩ 뮤지컬 희망      (조건부확률의 분자가 되는 핵심 칸)
  p01 = 영화 희망 ∩ 뮤지컬 비희망    (p11 과 함께 분모 "영화 희망 전체"를 이룸)
  p10 = 영화 비희망 ∩ 뮤지컬 희망    (표를 완성하는 나머지 칸 — 답에는 관여하지 않음)
  p00 = 영화 비희망 ∩ 뮤지컬 비희망  (표를 완성하는 나머지 칸)

  value(prm) = p11 / (p11 + p01)   → 조건부확률 정의식 P(A|B)=N(A∩B)/N(B) 그대로 계산.

  객관식 보기는 실제 평가원 문항의 전형적 생성 패턴을 재현한다: 정답을 기약분수
  num/den 으로 만든 뒤 분모를 2배(base_den)로 늘리고, 분자를 기준으로 연속된 정수
  5개를 나열한다(원문제: 3,4,5,6,7 / 14 → ①3/14 ②2/7 ③5/14 ④3/7 ⑤1/2). 정답이
  그 5개 중 몇 번째에 놓이는지(offset)는 "기약분수 분자를 5로 나눈 나머지"로 정해
  진다 — p11, p01 이 바뀌면 값(과 그 분자)이 바뀌므로 정답 번호도 함께 바뀐다.
  즉 p11, p01 두 파라미터가 모두 최종 정답 번호를 실제로 바꾸는 손잡이다.
"""
from sympy import Rational

CANDIDATE = 4  # 원문제 정답: ④

PARAMS = dict(
    p11=90,   # 영화 희망 ∩ 뮤지컬 희망
    p01=120,  # 영화 희망 ∩ 뮤지컬 비희망
    p10=50,   # 영화 비희망 ∩ 뮤지컬 희망
    p00=40,   # 영화 비희망 ∩ 뮤지컬 비희망
)


def value(prm):
    """조건부확률 P(뮤지컬 희망 | 영화 희망) = N(영화∩뮤지컬 희망) / N(영화 희망)."""
    p11, p01 = prm['p11'], prm['p01']
    denom = p11 + p01
    if p11 < 0 or p01 < 0 or denom <= 0:
        raise ValueError('영화 희망 학생 수가 존재하지 않아 조건부확률을 정의할 수 없음')
    return Rational(p11, denom)


def choices(prm):
    """값을 기약분수 num/den 으로 만들고 분모를 2배(base_den)로 늘린 뒤, 분자를
    기준으로 연속된 정수 5개를 나열해 보기를 만든다. 정답이 그중 몇 번째에 놓이는지
    (offset)는 분자를 5로 나눈 나머지로 정해지므로, 값이 바뀌면 위치도 함께 바뀐다."""
    v = value(prm)
    num, den = int(v.p), int(v.q)
    base_den = 2 * den
    offset = num % 5
    return [Rational(2 * num - offset + i, base_den) for i in range(5)]


def solve(prm):
    """정답이 보기 중 몇 번째(①=1 ... ⑤=5)에 놓이는지 — 문제의 '정답 번호'."""
    v = value(prm)
    opts = choices(prm)
    return opts.index(v) + 1


def statement(prm):
    p11, p01, p10, p00 = prm['p11'], prm['p01'], prm['p10'], prm['p00']
    row1, row2 = p11 + p01, p10 + p00
    col1, col2 = p11 + p10, p01 + p00
    total = row1 + row2
    return (
        f"어느 고등학교 3학년 전체 학생 {total}명을 대상으로 영화와 뮤지컬에 대한 "
        f"관람 희망 여부를 조사한 결과는 다음과 같다.\n\n"
        f"(단위: 명)\n"
        f"영화\\뮤지컬 | 희망함 | 희망하지 않음 | 합계\n"
        f"희망함      | {p11} | {p01} | {row1}\n"
        f"희망하지 않음 | {p10} | {p00} | {row2}\n"
        f"합계        | {col1} | {col2} | {total}\n\n"
        f"이 고등학교 3학년 학생 중에서 임의로 선택한 1명이 영화 관람을 희망한 "
        f"학생일 때, 이 학생이 뮤지컬 관람도 희망한 학생일 확률은?"
    )


# 원문제 보기(①~⑤)와 정확히 일치하는지 고정
assert choices(PARAMS) == [
    Rational(3, 14), Rational(2, 7), Rational(5, 14), Rational(3, 7), Rational(1, 2),
]

# 참고: 서로 다른 정답 번호를 내는 파라미터 조합들 — solve() 가 실제로 움직임을 보여줌
#   dict(PARAMS, p11=91)  → 91/211, num=91, offset=1 → 정답 ②
#   dict(PARAMS, p01=121) → 90/211, num=90, offset=0 → 정답 ①

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
