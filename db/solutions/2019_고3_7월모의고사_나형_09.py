"""
[원문제] 9번 (확률과 통계, 3점)
두 사건 A, B가 서로 독립이고 P(A)=1/3, P(A^C)=7*P(A∩B) 일 때 P(B)의 값은?
① 1/7 ② 2/7 ③ 3/7 ④ 4/7 ⑤ 5/7   → 정답 ②(=2/7)

[수학 구조]
  A, B 독립 ⇒ P(A∩B) = P(A)·P(B)
  P(A^C) = 1 - P(A)
  조건: 1 - P(A) = k · P(A)·P(B)   (원문제는 k=7)
  ⇒ P(B) = (1 - P(A)) / (k · P(A))

  파라미터로 뽑아낸 값:
    - P(A) = pA_num/pA_den  (원문제 1/3)
    - k = P(A^C) = k · P(A∩B) 식의 배수 계수 (원문제 7)
  두 값 모두 답 P(B)를 실제로 바꾼다 (묶여있지 않고 각자 독립적으로 흔들 수 있음).

  보기(①~⑤)는 원문제에서 "분모가 P(B)의 분모와 같고 분자가 1~5" 인 다섯 개의
  분수로 구성되어 있다. 이 구조를 그대로 살려 choices(prm) 을 value(prm) 에서
  유도한다: value 를 기약분수 num/den 으로 쪼개, num 이 1~5 사이 정수이면
  {1/den, 2/den, ..., 5/den} 을 보기로 삼고 num 번째가 정답이다.
"""
from sympy import Rational, symbols, Eq, solve as sp_solve

CANDIDATE = 2  # ★원문제 정답(보기 번호, ②) — 절대 바꾸지 않는다

PARAMS = dict(
    pA_num=1,   # P(A) 의 분자
    pA_den=3,   # P(A) 의 분모
    k=7,        # P(A^C) = k * P(A∩B) 의 배수 계수
)


def value(prm):
    """조건식을 풀어 P(B) 를 구한다 (수학 구조 자체를 sympy 로 계산)."""
    pA_num, pA_den, k = prm['pA_num'], prm['pA_den'], prm['k']
    pA = Rational(pA_num, pA_den)
    if not (0 < pA < 1):
        raise ValueError(f'P(A)={pA} 는 확률이 아니다 (0<P(A)<1 이어야 함)')
    if k <= 0:
        raise ValueError(f'k={k} 는 양수여야 한다')

    PB = symbols('PB', positive=True)
    PAc = 1 - pA                 # 여사건 확률
    PAB = pA * PB                # 독립사건 곱셈 정리 P(A∩B)=P(A)P(B)
    sol = sp_solve(Eq(PAc, k * PAB), PB)
    if not sol:
        raise ValueError('해가 존재하지 않는다')
    pb = sol[0]
    if not (0 < pb <= 1):
        raise ValueError(f'P(B)={pb} 가 확률 범위를 벗어난다')
    return pb


def choices(prm):
    """value(prm) 에서 보기 5개를 유도한다: 같은 분모, 분자 1~5."""
    v = value(prm)
    num, den = v.as_numer_denom()
    if not (num.is_Integer and 1 <= int(num) <= 5):
        raise ValueError(f'값 {v} 로는 1~5 번째 보기 구조를 만들 수 없다')
    return [Rational(i, den) for i in range(1, 6)]


def solve(prm):
    """값을 보기 목록에서 찾아 몇 번째 보기인지(1-indexed) 반환한다."""
    v = value(prm)
    ch = choices(prm)
    return ch.index(v) + 1


def statement(prm):
    pA = Rational(prm['pA_num'], prm['pA_den'])
    k = prm['k']
    ch = choices(prm)
    marks = ['①', '②', '③', '④', '⑤']
    ch_text = ' '.join(f'{m} {c}' for m, c in zip(marks, ch))
    return (
        f"두 사건 A, B가 서로 독립이고 P(A)={pA}, P(A^C)={k}P(A∩B) 일 때 "
        f"P(B)의 값은? (단, A^C는 A의 여사건이다.)\n{ch_text}"
    )


# 원문제 보기가 그대로 재현되는지 고정
assert choices(PARAMS) == [Rational(1, 7), Rational(2, 7), Rational(3, 7), Rational(4, 7), Rational(5, 7)]

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
